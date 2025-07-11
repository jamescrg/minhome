const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

function drawBootstrapBookmarkPlus(size) {
    const canvas = createCanvas(size, size);
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.clearRect(0, 0, size, size);

    // Bootstrap bookmark-plus SVG paths
    const path1 = "M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z";
    const path2 = "M8 4a.5.5 0 0 1 .5.5V6H10a.5.5 0 0 1 0 1H8.5v1.5a.5.5 0 0 1-1 0V7H6a.5.5 0 0 1 0-1h1.5V4.5A.5.5 0 0 1 8 4";

    const scale = size / 16;
    const limeGreen = '#65A30D'; // lime-600

    ctx.save();
    ctx.scale(scale, scale);
    ctx.fillStyle = limeGreen;

    // Create and draw the paths
    const p1 = new Path2D(path1);
    const p2 = new Path2D(path2);

    ctx.fill(p1);
    ctx.fill(p2);

    ctx.restore();

    return canvas;
}

// Generate icons in different sizes
const sizes = [
    { size: 16, filename: 'icon-16.png' },
    { size: 32, filename: 'icon-32.png' },
    { size: 48, filename: 'icon.png' },
    { size: 128, filename: 'icon-128.png' }
];

sizes.forEach(({ size, filename }) => {
    const canvas = drawBootstrapBookmarkPlus(size);
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(path.join(__dirname, filename), buffer);
    console.log(`Generated ${filename} (${size}x${size})`);
});

console.log('All icons generated successfully!');
