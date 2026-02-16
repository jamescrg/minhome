// Tiptap imports from local bundle (built with: npm run build)
import {
  Editor,
  Extension,
  Document,
  Paragraph,
  Text,
  Bold,
  Italic,
  Strike,
  Heading,
  BulletList,
  OrderedList,
  ListItem,
  Blockquote,
  HardBreak,
  History,
  Dropcursor,
  Gapcursor,
  Highlight,
  Plugin,
  PluginKey,
  Decoration,
  DecorationSet,
} from "./vendor/tiptap.bundle.js";

// Search highlight plugin for ProseMirror decorations
const searchPluginKey = new PluginKey("search");

const SearchHighlight = Extension.create({
  name: "searchHighlight",

  addProseMirrorPlugins() {
    return [
      new Plugin({
        key: searchPluginKey,
        state: {
          init() {
            return { searchTerm: "", decorations: DecorationSet.empty, matches: [] };
          },
          apply(tr, prev, oldState, newState) {
            const meta = tr.getMeta(searchPluginKey);
            if (meta !== undefined) {
              if (!meta.searchTerm) {
                return { searchTerm: "", decorations: DecorationSet.empty, matches: [] };
              }
              const decorations = [];
              const matches = [];
              const escapedTerm = meta.searchTerm.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
              const regex = new RegExp(escapedTerm, "gi");

              newState.doc.descendants(function(node, pos) {
                if (node.isText) {
                  const text = node.text;
                  let match;
                  while ((match = regex.exec(text)) !== null) {
                    const from = pos + match.index;
                    const to = from + match[0].length;
                    matches.push({ from: from, to: to });
                    const className = meta.currentIndex === matches.length - 1
                      ? "search-match search-match-current"
                      : "search-match";
                    decorations.push(
                      Decoration.inline(from, to, { class: className })
                    );
                  }
                }
              });

              return {
                searchTerm: meta.searchTerm,
                decorations: DecorationSet.create(newState.doc, decorations),
                matches: matches,
              };
            }
            // Map decorations through document changes
            const mapped = prev.decorations.map(tr.mapping, tr.doc);
            const mappedMatches = prev.matches.map(function(m) {
              return {
                from: tr.mapping.map(m.from),
                to: tr.mapping.map(m.to),
              };
            });
            return {
              searchTerm: prev.searchTerm,
              decorations: mapped,
              matches: mappedMatches,
            };
          },
        },
        props: {
          decorations(state) {
            return this.getState(state).decorations;
          },
        },
      }),
    ];
  },
});

let editor = null;
let autosaveTimer = null;
let lastSavedContent = "";

// Search state
let searchMatches = [];
let currentMatchIndex = -1;

// Initialize editor
function initEditor() {
  const container = document.getElementById("note-editor");
  if (!container || !window.NOTE_DATA) return;

  // Parse initial content - convert markdown to HTML
  let initialContent = window.NOTE_DATA.content || "";
  initialContent = markdownToHtml(initialContent);

  editor = new Editor({
    element: container,
    extensions: [
      Document,
      Paragraph,
      Text,
      Bold,
      Italic.extend({
        addKeyboardShortcuts() {
          return {
            "Mod-i": ({ editor, event }) => {
              // Don't handle if Shift is pressed (allow Ctrl+Shift+I for DevTools)
              if (event && event.shiftKey) {
                return false;
              }
              return editor.commands.toggleItalic();
            },
          };
        },
      }),
      Strike,
      Heading.configure({ levels: [1, 2, 3, 4, 5] }),
      BulletList,
      OrderedList,
      ListItem,
      Blockquote,
      HardBreak,
      History,
      Dropcursor,
      Gapcursor,
      Highlight.configure({ multicolor: true }),
      SearchHighlight,
    ],
    content: initialContent,
    autofocus: true,
    onUpdate: function () {
      scheduleAutosave();
      scheduleOutlineUpdate();
    },
  });

  lastSavedContent = getMarkdownContent();
  setupToolbar();
  setupKeyboardShortcuts();
  setupTitleEdit();
  setupSearchBar();
  setupImportExport();

  // Build heading outline
  buildOutline();
}

function setupTitleEdit() {
  const input = document.getElementById("note-title");
  if (!input) return;

  let originalTitle = input.value;

  input.addEventListener("blur", function () {
    const newTitle = input.value.trim();
    if (!newTitle) {
      input.value = originalTitle;
      return;
    }
    if (newTitle === originalTitle) return;

    // Save the new title
    const formData = new FormData();
    formData.append("title", newTitle);

    fetch(window.NOTE_DATA.titleUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.saved) {
          originalTitle = data.title;
          input.value = data.title;
        } else {
          input.value = originalTitle;
        }
      })
      .catch(() => {
        input.value = originalTitle;
      });
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      input.blur();
    } else if (e.key === "Escape") {
      e.preventDefault();
      input.value = originalTitle;
      input.blur();
    }
  });
}

// Convert simple markdown to HTML for editor
function markdownToHtml(md) {
  if (!md) return "<p></p>";

  function formatInline(text) {
    return text
      .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.+?)\*/g, "<em>$1</em>")
      .replace(/~~(.+?)~~/g, "<s>$1</s>")
      // Colored highlights: g==, r==, p==, o==, c==, a==
      .replace(/g==(.+?)==/g, '<mark data-color="mark-green">$1</mark>')
      .replace(/r==(.+?)==/g, '<mark data-color="mark-red">$1</mark>')
      .replace(/p==(.+?)==/g, '<mark data-color="mark-purple">$1</mark>')
      .replace(/o==(.+?)==/g, '<mark data-color="mark-orange">$1</mark>')
      .replace(/c==(.+?)==/g, '<mark data-color="mark-citation">$1</mark>')
      .replace(/a==(.+?)==/g, '<mark data-color="mark-gray">$1</mark>')
      // Default highlight: ==text==
      .replace(/==(.+?)==/g, "<mark>$1</mark>");
  }

  // Parse lines into list items with depth info
  // Handle both Unix (\n) and Windows (\r\n) line endings
  const lines = md.split(/\r?\n/);
  const parsed = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      parsed.push({ type: "blank" });
      continue;
    }

    // Check for headers
    const headerMatch = trimmed.match(/^(#{1,5}) (.+)$/);
    if (headerMatch) {
      parsed.push({
        type: "header",
        level: headerMatch[1].length,
        content: formatInline(headerMatch[2]),
      });
      continue;
    }

    // Check for blockquote
    if (trimmed.startsWith("> ")) {
      parsed.push({
        type: "blockquote",
        content: formatInline(trimmed.substring(2)),
      });
      continue;
    }

    // Check for unordered list item
    const ulMatch = line.replace(/\r$/, "").match(/^([ \t]*)[-*] (.*)$/);
    if (ulMatch) {
      const indentStr = ulMatch[1].replace(/\t/g, "  ");
      const depth = Math.floor(indentStr.length / 2);
      parsed.push({
        type: "li",
        listType: "ul",
        depth: depth,
        content: formatInline(ulMatch[2] || ""),
      });
      continue;
    }

    // Check for ordered list item
    const olMatch = line.replace(/\r$/, "").match(/^([ \t]*)(\d+)\. (.*)$/);
    if (olMatch) {
      const indentStr = olMatch[1].replace(/\t/g, "  ");
      const depth = Math.floor(indentStr.length / 2);
      parsed.push({
        type: "li",
        listType: "ol",
        depth: depth,
        content: formatInline(olMatch[3] || ""),
      });
      continue;
    }

    // Regular paragraph
    parsed.push({
      type: "paragraph",
      content: formatInline(trimmed),
    });
  }

  // Build HTML with proper nesting for ProseMirror
  const result = [];
  let i = 0;

  function buildList(startIndex, minDepth) {
    let idx = startIndex;
    const items = [];

    while (idx < parsed.length) {
      const item = parsed[idx];

      if (item.type !== "li") {
        break;
      }

      if (item.depth < minDepth) {
        break;
      }

      if (item.depth === minDepth) {
        const listType = item.listType;
        let liContent = "<li><p>" + item.content + "</p>";
        idx++;

        // Check if next items are nested (deeper)
        if (idx < parsed.length && parsed[idx].type === "li" && parsed[idx].depth > minDepth) {
          const nested = buildList(idx, parsed[idx].depth);
          liContent += nested.html;
          idx = nested.endIndex;
        }

        liContent += "</li>";
        items.push({ html: liContent, listType: listType });
      } else {
        break;
      }
    }

    if (items.length === 0) {
      return { html: "", endIndex: idx };
    }

    const listType = items[0].listType;
    const html = "<" + listType + ">" + items.map(function(it) { return it.html; }).join("") + "</" + listType + ">";

    return { html: html, endIndex: idx };
  }

  while (i < parsed.length) {
    const item = parsed[i];

    if (item.type === "blank") {
      i++;
      continue;
    }

    if (item.type === "header") {
      result.push("<h" + item.level + ">" + item.content + "</h" + item.level + ">");
      i++;
      continue;
    }

    if (item.type === "blockquote") {
      result.push("<blockquote><p>" + item.content + "</p></blockquote>");
      i++;
      continue;
    }

    if (item.type === "paragraph") {
      result.push("<p>" + item.content + "</p>");
      i++;
      continue;
    }

    if (item.type === "li") {
      const listResult = buildList(i, item.depth);
      result.push(listResult.html);
      i = listResult.endIndex;
      continue;
    }

    i++;
  }

  return result.join("") || "<p></p>";
}

// Convert editor HTML to markdown
function htmlToMarkdown(html) {
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = html;

  function processNode(node, listDepth, listType, listIndex) {
    if (node.nodeType === Node.TEXT_NODE) {
      return node.textContent;
    }

    if (node.nodeType !== Node.ELEMENT_NODE) return "";

    const tag = node.tagName.toLowerCase();

    function getChildren() {
      return Array.from(node.childNodes).map(function(child) {
        return processNode(child, listDepth, null, 0);
      }).join("");
    }

    switch (tag) {
      case "h1":
        return "# " + getChildren() + "\n\n";
      case "h2":
        return "## " + getChildren() + "\n\n";
      case "h3":
        return "### " + getChildren() + "\n\n";
      case "h4":
        return "#### " + getChildren() + "\n\n";
      case "h5":
        return "##### " + getChildren() + "\n\n";
      case "p":
        if (listDepth > 0) {
          return getChildren();
        }
        return getChildren() + "\n\n";
      case "strong":
        return "**" + getChildren() + "**";
      case "em":
        return "*" + getChildren() + "*";
      case "s":
        return "~~" + getChildren() + "~~";
      case "mark": {
        const markColor = node.dataset.color || "";
        if (node.classList.contains("mark-green") || markColor === "mark-green")
          return "g==" + getChildren() + "==";
        if (node.classList.contains("mark-red") || markColor === "mark-red")
          return "r==" + getChildren() + "==";
        if (node.classList.contains("mark-purple") || markColor === "mark-purple")
          return "p==" + getChildren() + "==";
        if (node.classList.contains("mark-orange") || markColor === "mark-orange")
          return "o==" + getChildren() + "==";
        if (node.classList.contains("mark-citation") || markColor === "mark-citation")
          return "c==" + getChildren() + "==";
        if (node.classList.contains("mark-gray") || markColor === "mark-gray")
          return "a==" + getChildren() + "==";
        return "==" + getChildren() + "==";
      }
      case "blockquote":
        return (
          getChildren()
            .trim()
            .split("\n")
            .map(function (line) {
              return "> " + line;
            })
            .join("\n") + "\n\n"
        );
      case "ul":
      case "ol": {
        let result = "";
        let idx = 1;
        Array.from(node.children).forEach(function(child) {
          if (child.tagName.toLowerCase() === "li") {
            result += processNode(child, listDepth + 1, tag, idx);
            idx++;
          }
        });
        if (listDepth === 0) {
          result += "\n";
        }
        return result;
      }
      case "li": {
        const indent = "  ".repeat(listDepth - 1);
        let prefix;
        if (listType === "ol") {
          prefix = listIndex + ". ";
        } else {
          prefix = "- ";
        }

        let textContent = "";
        let nestedLists = "";

        Array.from(node.childNodes).forEach(function(child) {
          if (child.nodeType === Node.ELEMENT_NODE) {
            const childTag = child.tagName.toLowerCase();
            if (childTag === "ul" || childTag === "ol") {
              nestedLists += processNode(child, listDepth, null, 0);
            } else {
              textContent += processNode(child, listDepth, null, 0);
            }
          } else {
            textContent += processNode(child, listDepth, null, 0);
          }
        });

        return indent + prefix + textContent.trim() + "\n" + nestedLists;
      }
      case "br":
        return "\n";
      default:
        return getChildren();
    }
  }

  let markdown = processNode(tempDiv, 0, null, 0);
  markdown = markdown.replace(/\n{3,}/g, "\n\n").trim();
  return markdown;
}

function getMarkdownContent() {
  if (!editor) return "";
  const html = editor.getHTML();
  return htmlToMarkdown(html);
}

// Autosave with debounce
function scheduleAutosave() {
  if (autosaveTimer) clearTimeout(autosaveTimer);
  updateSaveStatus("unsaved");
  autosaveTimer = setTimeout(performAutosave, 2000);
}

function performAutosave() {
  const content = getMarkdownContent();
  if (content === lastSavedContent) {
    updateSaveStatus("saved");
    return;
  }

  updateSaveStatus("saving");

  const formData = new FormData();
  formData.append("content", content);

  fetch(window.NOTE_DATA.autosaveUrl, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
    body: formData,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.saved) {
        lastSavedContent = content;
        updateSaveStatus("saved");
      }
    })
    .catch(function () {
      updateSaveStatus("unsaved");
    });
}

function updateSaveStatus(status) {
  const btn = document.getElementById("save-status-btn");
  if (!btn) return;

  const icon = btn.querySelector("i");
  if (!icon) return;

  if (status === "unsaved") {
    btn.classList.add("active");
    btn.title = "Unsaved changes";
    icon.className = "icon-cloud-upload";
  } else if (status === "saving") {
    btn.classList.add("active");
    btn.title = "Saving...";
    icon.className = "icon-cloud-upload";
  } else {
    btn.classList.remove("active");
    btn.title = "Saved";
    icon.className = "icon-cloud";
  }
}

function getCSRFToken() {
  const el = document.querySelector("[name=csrfmiddlewaretoken]");
  return el ? el.value : "";
}

// Toolbar setup
function setupToolbar() {
  const btnBold = document.getElementById("btn-bold");
  const btnItalic = document.getElementById("btn-italic");
  const btnStrike = document.getElementById("btn-strike");
  const btnH1 = document.getElementById("btn-heading-1");
  const btnH2 = document.getElementById("btn-heading-2");
  const btnH3 = document.getElementById("btn-heading-3");
  const btnBullet = document.getElementById("btn-bullet-list");
  const btnOrdered = document.getElementById("btn-ordered-list");
  const btnQuote = document.getElementById("btn-blockquote");

  if (btnBold) {
    btnBold.addEventListener("click", function () {
      editor.chain().focus().toggleBold().run();
    });
  }
  if (btnItalic) {
    btnItalic.addEventListener("click", function () {
      editor.chain().focus().toggleItalic().run();
    });
  }
  if (btnStrike) {
    btnStrike.addEventListener("click", function () {
      editor.chain().focus().toggleStrike().run();
    });
  }
  if (btnH1) {
    btnH1.addEventListener("click", function () {
      editor.chain().focus().toggleHeading({ level: 1 }).run();
    });
  }
  if (btnH2) {
    btnH2.addEventListener("click", function () {
      editor.chain().focus().toggleHeading({ level: 2 }).run();
    });
  }
  if (btnH3) {
    btnH3.addEventListener("click", function () {
      editor.chain().focus().toggleHeading({ level: 3 }).run();
    });
  }
  if (btnBullet) {
    btnBullet.addEventListener("click", function () {
      editor.chain().focus().toggleBulletList().run();
    });
  }
  if (btnOrdered) {
    btnOrdered.addEventListener("click", function () {
      editor.chain().focus().toggleOrderedList().run();
    });
  }
  if (btnQuote) {
    btnQuote.addEventListener("click", function () {
      editor.chain().focus().toggleBlockquote().run();
    });
  }
}

function setupKeyboardShortcuts() {
  document.addEventListener("keydown", function (e) {
    const mod = e.ctrlKey || e.metaKey;

    // Save: Ctrl+S
    if (mod && e.key === "s") {
      e.preventDefault();
      if (autosaveTimer) clearTimeout(autosaveTimer);
      performAutosave();
      return;
    }

    // Headings: Ctrl+1 through Ctrl+5
    if (mod && !e.shiftKey && e.key === "1") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 1 }).run();
      return;
    }
    if (mod && !e.shiftKey && e.key === "2") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 2 }).run();
      return;
    }
    if (mod && !e.shiftKey && e.key === "3") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 3 }).run();
      return;
    }
    if (mod && !e.shiftKey && e.key === "4") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 4 }).run();
      return;
    }
    if (mod && !e.shiftKey && e.key === "5") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 5 }).run();
      return;
    }

    // Clear formatting / convert to paragraph: Ctrl+0
    if (mod && !e.shiftKey && e.key === "0") {
      e.preventDefault();
      editor.chain().focus().setParagraph().run();
      return;
    }

    // F-key shortcuts for headings: F2, F3, F4
    if (e.key === "F2") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 2 }).run();
      return;
    }
    if (e.key === "F3") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 3 }).run();
      return;
    }
    if (e.key === "F4") {
      e.preventDefault();
      editor.chain().focus().toggleHeading({ level: 4 }).run();
      return;
    }

    // F7 for bullet list
    if (e.key === "F7") {
      e.preventDefault();
      editor.chain().focus().toggleBulletList().run();
      return;
    }

    // Bullet list: Ctrl+7
    if (mod && !e.shiftKey && e.key === "7") {
      e.preventDefault();
      editor.chain().focus().toggleBulletList().run();
      return;
    }

    // Blockquote: Ctrl+8
    if (mod && !e.shiftKey && e.key === "8") {
      e.preventDefault();
      editor.chain().focus().toggleBlockquote().run();
      return;
    }

    // Move list item up: Ctrl+Up
    if (mod && e.key === "ArrowUp" && editor.isActive("listItem")) {
      e.preventDefault();
      moveListItem("up");
      return;
    }

    // Move list item down: Ctrl+Down
    if (mod && e.key === "ArrowDown" && editor.isActive("listItem")) {
      e.preventDefault();
      moveListItem("down");
      return;
    }

    // Delete block/list item: Ctrl+Delete or Ctrl+D
    if (mod && (e.key === "Delete" || e.key === "d")) {
      e.preventDefault();
      editor.chain().focus().deleteNode("paragraph").run();
      return;
    }

    // Show shortcuts: Ctrl+?
    if (mod && e.key === "?") {
      e.preventDefault();
      showShortcutsModal();
      return;
    }

    // Highlight shortcuts: Alt+Y (yellow), Alt+G (green), Alt+R (red), Alt+P (purple), Alt+O (orange), Alt+A (gray)
    if (e.altKey && !mod && ["y", "g", "r", "p", "o", "a"].includes(e.key.toLowerCase())) {
      e.preventDefault();
      const colorMap = {
        y: null, // default yellow
        g: "mark-green",
        r: "mark-red",
        p: "mark-purple",
        o: "mark-orange",
        a: "mark-gray",
      };
      const color = colorMap[e.key.toLowerCase()];
      if (color) {
        editor.chain().focus().toggleHighlight({ color }).run();
      } else {
        editor.chain().focus().toggleHighlight().run();
      }
      return;
    }

    // Remove highlight: Alt+C
    if (e.altKey && !mod && e.key.toLowerCase() === "c") {
      e.preventDefault();
      editor.chain().focus().unsetHighlight().run();
      return;
    }

    // Search and replace: Ctrl+H
    if (mod && e.key === "h") {
      e.preventDefault();
      toggleSearchBar();
      return;
    }
  });
}

function showShortcutsModal() {
  const btn = document.querySelector('[title="Keyboard shortcuts"]');
  if (btn) {
    btn.click();
  }
}

function moveListItem(direction) {
  const { state, view } = editor;
  const { selection } = state;
  const { $from } = selection;

  let listItemPos = null;
  let listItemNode = null;
  let listItemDepth = null;

  for (let d = $from.depth; d > 0; d--) {
    const node = $from.node(d);
    if (node.type.name === "listItem") {
      listItemPos = $from.before(d);
      listItemNode = node;
      listItemDepth = d;
      break;
    }
  }

  if (!listItemNode || listItemPos === null) return;

  const parentList = $from.node(listItemDepth - 1);
  const indexInParent = $from.index(listItemDepth - 1);

  if (direction === "up" && indexInParent === 0) return;
  if (direction === "down" && indexInParent >= parentList.childCount - 1) return;

  const tr = state.tr;
  const listItemEnd = listItemPos + listItemNode.nodeSize;
  let newCursorPos;

  if (direction === "up") {
    const prevItemNode = parentList.child(indexInParent - 1);
    const prevItemSize = prevItemNode.nodeSize;
    newCursorPos = $from.pos - prevItemSize;
    const slice = tr.doc.slice(listItemPos, listItemEnd);
    tr.delete(listItemPos, listItemEnd);
    tr.insert(listItemPos - prevItemSize, slice.content);
  } else {
    const nextItemNode = parentList.child(indexInParent + 1);
    const nextItemSize = nextItemNode.nodeSize;
    newCursorPos = $from.pos + nextItemSize;
    const nextItemPos = listItemEnd;
    const nextSlice = tr.doc.slice(nextItemPos, nextItemPos + nextItemSize);
    tr.delete(nextItemPos, nextItemPos + nextItemSize);
    tr.insert(listItemPos, nextSlice.content);
  }

  tr.setSelection(state.selection.constructor.near(tr.doc.resolve(newCursorPos)));
  view.dispatch(tr.scrollIntoView());
}

// =============================================================================
// Search and Replace
// =============================================================================

function setupSearchBar() {
  const searchInput = document.getElementById("search-input");
  const replaceInput = document.getElementById("replace-input");
  const prevBtn = document.getElementById("search-prev");
  const nextBtn = document.getElementById("search-next");
  const replaceBtn = document.getElementById("replace-one");
  const replaceAllBtn = document.getElementById("replace-all");
  const closeBtn = document.getElementById("search-close");
  const toggleBtn = document.getElementById("search-toggle-btn");

  if (searchInput) {
    let searchTimer;
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(function () {
        performSearch(searchInput.value);
      }, 200);
    });

    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        goToNextMatch();
      } else if (e.key === "Escape") {
        hideSearchBar();
      }
    });
  }

  if (replaceInput) {
    replaceInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        replaceCurrentMatch();
      } else if (e.key === "Escape") {
        hideSearchBar();
      }
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", goToPrevMatch);
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", goToNextMatch);
  }

  if (replaceBtn) {
    replaceBtn.addEventListener("click", replaceCurrentMatch);
  }

  if (replaceAllBtn) {
    replaceAllBtn.addEventListener("click", replaceAllMatches);
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", hideSearchBar);
  }

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function (e) {
      e.preventDefault();
      toggleSearchBar();
    });
  }
}

function toggleSearchBar() {
  const bar = document.getElementById("search-replace-bar");
  if (bar && bar.classList.contains("visible")) {
    hideSearchBar();
  } else {
    showSearchBar();
  }
}

function showSearchBar() {
  const bar = document.getElementById("search-replace-bar");
  const searchInput = document.getElementById("search-input");
  const toggleBtn = document.getElementById("search-toggle-btn");

  if (bar) {
    bar.classList.add("visible");
  }
  if (toggleBtn) {
    toggleBtn.classList.add("active");
  }
  if (searchInput) {
    searchInput.focus();
    searchInput.select();
  }
}

function hideSearchBar() {
  const bar = document.getElementById("search-replace-bar");
  const toggleBtn = document.getElementById("search-toggle-btn");
  const searchInput = document.getElementById("search-input");
  const replaceInput = document.getElementById("replace-input");

  if (bar) {
    bar.classList.remove("visible");
  }
  if (toggleBtn) {
    toggleBtn.classList.remove("active");
  }

  clearSearchHighlights();
  searchMatches = [];
  currentMatchIndex = -1;
  updateSearchCount();

  if (searchInput) searchInput.value = "";
  if (replaceInput) replaceInput.value = "";

  if (editor) {
    editor.commands.focus();
  }
}

function performSearch(searchTerm) {
  searchMatches = [];
  currentMatchIndex = -1;

  if (!searchTerm || !editor) {
    const tr = editor.state.tr;
    tr.setMeta(searchPluginKey, { searchTerm: "", currentIndex: -1 });
    editor.view.dispatch(tr);
    updateSearchCount();
    return;
  }

  const tr = editor.state.tr;
  tr.setMeta(searchPluginKey, { searchTerm: searchTerm, currentIndex: 0 });
  editor.view.dispatch(tr);

  const pluginState = searchPluginKey.getState(editor.state);
  if (pluginState && pluginState.matches) {
    searchMatches = pluginState.matches;
  }

  if (searchMatches.length > 0) {
    currentMatchIndex = 0;
    scrollToCurrentMatch();
  }

  updateSearchCount();
}

function clearSearchHighlights() {
  if (!editor) return;

  const tr = editor.state.tr;
  tr.setMeta(searchPluginKey, { searchTerm: "", currentIndex: -1 });
  editor.view.dispatch(tr);

  searchMatches = [];
  currentMatchIndex = -1;
}

function updateSearchDecorations() {
  if (!editor) return;

  const searchInput = document.getElementById("search-input");
  const searchTerm = searchInput ? searchInput.value : "";

  const tr = editor.state.tr;
  tr.setMeta(searchPluginKey, { searchTerm: searchTerm, currentIndex: currentMatchIndex });
  editor.view.dispatch(tr);
}

function scrollToCurrentMatch() {
  if (currentMatchIndex < 0 || currentMatchIndex >= searchMatches.length) return;

  requestAnimationFrame(function() {
    const currentMatchEl = document.querySelector(".search-match-current");
    if (!currentMatchEl) return;

    const notePage = document.querySelector(".note-page");
    if (notePage) {
      const matchRect = currentMatchEl.getBoundingClientRect();
      const containerRect = notePage.getBoundingClientRect();
      const centerOffset = notePage.clientHeight / 2;
      const scrollTop = notePage.scrollTop + (matchRect.top - containerRect.top) - centerOffset;
      notePage.scrollTo({ top: Math.max(0, scrollTop), behavior: "smooth" });
    }
  });
}

function updateSearchCount() {
  const countEl = document.getElementById("search-count");
  if (countEl) {
    if (searchMatches.length === 0) {
      countEl.textContent = "";
    } else {
      countEl.textContent = (currentMatchIndex + 1) + " of " + searchMatches.length;
    }
  }
}

function goToNextMatch() {
  if (searchMatches.length === 0) return;
  currentMatchIndex = (currentMatchIndex + 1) % searchMatches.length;
  updateSearchDecorations();
  scrollToCurrentMatch();
  updateSearchCount();
}

function goToPrevMatch() {
  if (searchMatches.length === 0) return;
  currentMatchIndex =
    (currentMatchIndex - 1 + searchMatches.length) % searchMatches.length;
  updateSearchDecorations();
  scrollToCurrentMatch();
  updateSearchCount();
}

function replaceCurrentMatch() {
  if (currentMatchIndex < 0 || currentMatchIndex >= searchMatches.length) return;

  const searchInput = document.getElementById("search-input");
  const replaceInput = document.getElementById("replace-input");
  if (!searchInput || !editor) return;

  const searchTerm = searchInput.value;
  const replaceTerm = replaceInput ? replaceInput.value : "";

  const match = searchMatches[currentMatchIndex];
  if (!match) return;

  editor
    .chain()
    .focus()
    .setTextSelection({ from: match.from, to: match.to })
    .deleteSelection()
    .insertContent(replaceTerm)
    .run();

  performSearch(searchTerm);
  scheduleAutosave();
}

function replaceAllMatches() {
  const searchInput = document.getElementById("search-input");
  const replaceInput = document.getElementById("replace-input");
  if (!searchInput || !editor) return;

  const searchTerm = searchInput.value;
  const replaceTerm = replaceInput ? replaceInput.value : "";

  if (!searchTerm || searchMatches.length === 0) return;

  const matchesCopy = searchMatches.slice().reverse();

  editor.chain().focus().run();

  matchesCopy.forEach(function(match) {
    editor
      .chain()
      .setTextSelection({ from: match.from, to: match.to })
      .deleteSelection()
      .insertContent(replaceTerm)
      .run();
  });

  clearSearchHighlights();
  updateSearchCount();
  scheduleAutosave();
}

// =============================================================================
// Import/Export
// =============================================================================

function setupImportExport() {
  const exportBtn = document.getElementById("export-btn");
  if (exportBtn) {
    exportBtn.addEventListener("click", function (e) {
      e.preventDefault();
      exportToMarkdown();
    });
  }

  document.body.addEventListener("htmx:afterSwap", function (e) {
    if (document.getElementById("import-confirm-btn")) {
      setupImportModal();
    }
  });
}

function exportToMarkdown() {
  if (!editor) return;

  const markdown = getMarkdownContent();
  const title = window.NOTE_DATA.title || "note";

  const safeTitle = title.replace(/[^a-zA-Z0-9 \-_]/g, "").trim() || "note";
  const filename = safeTitle + ".md";

  const blob = new Blob([markdown], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function setupImportModal() {
  const fileInput = document.getElementById("import-file");
  const textInput = document.getElementById("import-text");
  const confirmBtn = document.getElementById("import-confirm-btn");

  if (!fileInput || !textInput || !confirmBtn) return;

  fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
      textInput.value = e.target.result;
    };
    reader.readAsText(file);
  });

  confirmBtn.addEventListener("click", function () {
    const content = textInput.value.trim();
    if (!content) return;

    const replaceContent = document.getElementById("import-replace").checked;
    importMarkdown(content, replaceContent);

    // Close modal using Bootstrap
    const modal = bootstrap.Modal.getInstance(document.getElementById("htmx-modal-container"));
    if (modal) modal.hide();
  });
}

function importMarkdown(markdown, replace) {
  if (!editor) return;

  const html = markdownToHtml(markdown);

  if (replace) {
    editor.commands.setContent(html);
  } else {
    editor.commands.focus("end");
    editor.commands.insertContent("<p></p>" + html);
  }

  scheduleAutosave();
}

// =============================================================================
// Outline Panel - Heading Navigation
// =============================================================================

function buildOutline() {
  const outlineList = document.getElementById("outline-list");
  if (!outlineList || !editor) return;

  const headings = [];

  editor.state.doc.descendants(function(node, pos) {
    if (node.type.name === "heading" && node.attrs.level >= 2) {
      headings.push({
        level: node.attrs.level,
        text: node.textContent.trim(),
        pos: pos,
      });
    }
  });

  if (headings.length === 0) {
    outlineList.innerHTML = '<li class="outline-empty">No headings</li>';
    return;
  }

  const noteId = window.NOTE_DATA ? window.NOTE_DATA.id : "default";
  const storageKey = "outline-collapsed-" + noteId;
  let collapsedItems = [];
  try {
    collapsedItems = JSON.parse(localStorage.getItem(storageKey)) || [];
  } catch (e) {
    collapsedItems = [];
  }

  function buildHierarchicalHtml(headings) {
    let html = "";
    let i = 0;

    while (i < headings.length) {
      const heading = headings[i];
      const text = heading.text || "(empty)";

      const children = [];
      let j = i + 1;
      while (j < headings.length && headings[j].level > heading.level) {
        children.push(headings[j]);
        j++;
      }

      const hasChildren = children.length > 0;
      const isCollapsed = collapsedItems.includes(heading.pos);
      const collapsedClass = isCollapsed ? " collapsed" : "";

      if (hasChildren) {
        html += '<li class="outline-item has-children level-' + heading.level + collapsedClass + '" data-pos="' + heading.pos + '">';
        html += '<span class="outline-toggle"><i class="icon-chevron-down"></i></span>';
        html += '<span class="outline-text">' + text + '</span>';
        html += '<ul class="outline-children">';
        html += buildHierarchicalHtml(children);
        html += '</ul>';
        html += '</li>';
      } else {
        html += '<li class="outline-item level-' + heading.level + '" data-pos="' + heading.pos + '">';
        html += '<span class="outline-toggle-spacer"></span>';
        html += '<span class="outline-text">' + text + '</span>';
        html += '</li>';
      }

      i = j;
    }

    return html;
  }

  outlineList.innerHTML = buildHierarchicalHtml(headings);

  outlineList.querySelectorAll(".outline-toggle").forEach(function(toggle) {
    toggle.addEventListener("click", function(e) {
      e.stopPropagation();
      const item = toggle.closest(".outline-item");
      if (!item) return;

      item.classList.toggle("collapsed");

      const pos = parseInt(item.dataset.pos, 10);
      if (item.classList.contains("collapsed")) {
        if (!collapsedItems.includes(pos)) {
          collapsedItems.push(pos);
        }
      } else {
        collapsedItems = collapsedItems.filter(function(p) { return p !== pos; });
      }
      localStorage.setItem(storageKey, JSON.stringify(collapsedItems));
    });
  });

  outlineList.querySelectorAll(".outline-text").forEach(function(textEl) {
    textEl.addEventListener("click", function() {
      const item = textEl.closest(".outline-item");
      if (!item) return;
      const pos = parseInt(item.dataset.pos, 10);
      scrollToHeading(pos);
    });
  });

  outlineList.querySelectorAll(".outline-item:not(.has-children)").forEach(function(item) {
    if (!item.querySelector(".outline-toggle")) {
      item.style.cursor = "pointer";
      item.addEventListener("click", function() {
        const pos = parseInt(item.dataset.pos, 10);
        scrollToHeading(pos);
      });
    }
  });

  updateCollapseButtonIcon();
}

function scrollToHeading(pos) {
  if (!editor) return;

  const domAtPos = editor.view.domAtPos(pos + 1);
  if (domAtPos && domAtPos.node) {
    let element = domAtPos.node;
    if (element.nodeType === Node.TEXT_NODE) {
      element = element.parentElement;
    }
    const heading = element.closest("h1, h2, h3, h4, h5, h6");
    if (heading) {
      const notePage = document.querySelector(".note-page");
      if (notePage) {
        const headingRect = heading.getBoundingClientRect();
        const containerRect = notePage.getBoundingClientRect();
        const scrollTop = notePage.scrollTop + (headingRect.top - containerRect.top) - 32;
        notePage.scrollTo({ top: Math.max(0, scrollTop), behavior: "smooth" });
      }
    }
  }
}

// Debounced outline update
let outlineTimer = null;
function scheduleOutlineUpdate() {
  if (outlineTimer) clearTimeout(outlineTimer);
  outlineTimer = setTimeout(buildOutline, 500);
}

// Collapse/Expand all outline items
function setupOutlineCollapseAll() {
  const btn = document.getElementById("outline-collapse-btn");
  if (!btn) return;

  btn.addEventListener("click", function() {
    const outlineList = document.getElementById("outline-list");
    if (!outlineList) return;

    const collapsibleItems = outlineList.querySelectorAll(".outline-item.has-children");
    if (collapsibleItems.length === 0) return;

    const allCollapsed = Array.from(collapsibleItems).every(function(item) {
      return item.classList.contains("collapsed");
    });

    const noteId = window.NOTE_DATA ? window.NOTE_DATA.id : "default";
    const storageKey = "outline-collapsed-" + noteId;
    let collapsedPositions = [];

    collapsibleItems.forEach(function(item) {
      if (allCollapsed) {
        item.classList.remove("collapsed");
      } else {
        item.classList.add("collapsed");
        const pos = parseInt(item.dataset.pos, 10);
        if (!isNaN(pos)) {
          collapsedPositions.push(pos);
        }
      }
    });

    localStorage.setItem(storageKey, JSON.stringify(collapsedPositions));
    updateCollapseButtonIcon();
  });
}

function updateCollapseButtonIcon() {
  const btn = document.getElementById("outline-collapse-btn");
  const outlineList = document.getElementById("outline-list");
  if (!btn || !outlineList) return;

  const icon = btn.querySelector("i");
  if (!icon) return;

  const collapsibleItems = outlineList.querySelectorAll(".outline-item.has-children");
  const allCollapsed = collapsibleItems.length > 0 && Array.from(collapsibleItems).every(function(item) {
    return item.classList.contains("collapsed");
  });

  icon.className = allCollapsed ? "icon-chevrons-up-down" : "icon-chevrons-down-up";
}

// =============================================================================
// HTMX Integration for Note Switching
// =============================================================================

function setupHtmxHandlers() {
  document.body.addEventListener("htmx:beforeRequest", function(e) {
    if (e.detail.target && e.detail.target.id === "note-editor-container") {
      if (autosaveTimer) clearTimeout(autosaveTimer);
      performAutosave();

      const clickedItem = e.detail.elt;
      if (clickedItem && clickedItem.dataset.noteId) {
        updateSidebarActive(clickedItem.dataset.noteId);
      }
    }
  });

  document.body.addEventListener("htmx:afterSwap", function(e) {
    if (e.detail.target && e.detail.target.id === "note-editor-container") {
      if (editor) {
        editor.destroy();
        editor = null;
      }

      lastSavedContent = "";
      searchMatches = [];
      currentMatchIndex = -1;

      setTimeout(function() {
        initEditor();
      }, 50);
    }
  });
}

function updateSidebarActive(noteId) {
  const sidebar = document.querySelector(".sidebar-notes-list");
  if (!sidebar) return;

  sidebar.querySelectorAll("li").forEach(function(item) {
    item.classList.remove("active");
  });

  const activeItem = sidebar.querySelector('li[data-note-id="' + noteId + '"]');
  if (activeItem) {
    activeItem.classList.add("active");
  }
}

// =============================================================================
// Panel Collapse Toggle
// =============================================================================

function togglePanel(panelClass) {
  const panel = document.querySelector("." + panelClass);
  if (!panel) return;

  const isVisible = panel.offsetWidth > 0;

  if (isVisible) {
    panel.classList.add("collapsed");
    panel.classList.remove("expanded");
    localStorage.setItem("notes-editor-" + panelClass, "collapsed");
  } else {
    panel.classList.remove("collapsed");
    panel.classList.add("expanded");
    localStorage.setItem("notes-editor-" + panelClass, "expanded");
  }
}

function restorePanelStates() {
  const screenWidth = window.innerWidth;

  const sidebarState = localStorage.getItem("notes-editor-note-sidebar");
  const sidebar = document.querySelector(".note-sidebar");
  if (sidebar) {
    if (sidebarState === "collapsed") {
      sidebar.classList.add("collapsed");
    } else if (sidebarState === "expanded" && screenWidth >= 1200) {
      sidebar.classList.add("expanded");
    }
  }

  const outlineState = localStorage.getItem("notes-editor-note-outline");
  const outline = document.querySelector(".note-outline");
  if (outline) {
    if (outlineState === "collapsed") {
      outline.classList.add("collapsed");
    } else if (outlineState === "expanded" && screenWidth >= 768) {
      outline.classList.add("expanded");
    }
  }
}

// Expose togglePanel globally for onclick handlers
window.togglePanel = togglePanel;

// Initialize on load
document.addEventListener("DOMContentLoaded", function() {
  restorePanelStates();
  initEditor();
  setupHtmxHandlers();
  setupOutlineCollapseAll();
});
