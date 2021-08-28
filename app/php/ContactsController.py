

def create(id):
    user_id = request.user.id
    page = 'contacts'
    action = '/contacts'
    edit = false
    activeFolderId = id
    folders = FoldersController::getAll('contacts')
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    contact = new Contact
    contact.folder_id = id
    return view('contacts/content', context)


def update(Requests\CreateContactRequest request):

    # validation runs first

    # capture the input from the user
    input = request.all()

    # add the user's id
    input['user_id'] = request.user.id

    # make the contact that has been submitted the selected contact
    input['selected'] = 1

    # de-select the prior selected contact
    Contact.objects.filter(user_id=input['user_id'], selected=1).update(selected=0)

    # insert the new contact into the database
    Contact::create(input)

    # if google account is logged in
    # add to google contacts
    if (Auth::user().google_token) 

        # retrieve the most recent contact id (the one just added above)
        contactId = Contact.objects.filter('user_id', request.user.id).max('id')

        # retrieve the contact
        contact = Contact::findOrFail(contactId)

        # submit the contact to google and save the google_id as a property of the contact
        contact.google_id = GoogleContactHandler::add(contact)

        # save the contact with the google_id
        contact.save()


    return redirect('/contacts/')


def edit(id):

    user_id = request.user.id
    page = 'contacts'
    edit = true
    action = '/contacts/update/' . id
    folders = FoldersController::getAll('contacts')
    selectedFolder = Folder.objects.filter(user_id=user_id, page=page, selected=1).first()
    contact = Contact::findOrFail(id)
    return view('contacts/content', context)


def update(id, Requests\CreateContactRequest request):

    echo 'update contact'
    input = request.all()
    input['user_id'] = request.user.id
    contact = Contact.objects.filter(id=id, user_id=input['user_id']).first()

    # update contact in database
    contact.update(input)

    if (Auth::user().google_token) 

                # delete from google contacts if has contact id
    if contact.google_id:

        GoogleContactHandler::delete(contact.google_id)

        # add to google contacts
        input['google_id'] = GoogleContactHandler::add(contact)

        # update contact in database again (with google_id if logged in)
        contact.update(input)

        return redirect('/contacts/')


def destroy(id):
    user_id = request.user.id
    contact = Contact.objects.filter(id=id, user_id=user_id]).first()
    if (Auth::user().google_token) 

    if contact.google_id:
        GoogleContactHandler::delete(contact.google_id)
    contact.delete()
    return redirect('/contacts/')


