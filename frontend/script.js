// =======================================================
// ELEMENTS
// =======================================================

const fileInput =
    document.getElementById(
        "fileInput"
    );

const chooseFileButton =
    document.getElementById(
        "chooseFileButton"
    );

const uploadButton =
    document.getElementById(
        "uploadButton"
    );

const uploadArea =
    document.getElementById(
        "uploadArea"
    );

const selectedFile =
    document.getElementById(
        "selectedFile"
    );

const uploadStatus =
    document.getElementById(
        "uploadStatus"
    );

const documentSelect =
    document.getElementById(
        "documentSelect"
    );

const refreshDocuments =
    document.getElementById(
        "refreshDocuments"
    );

const deleteDocumentButton =
    document.getElementById(
        "deleteDocumentButton"
    );

const documentStatus =
    document.getElementById(
        "documentStatus"
    );

const questionInput =
    document.getElementById(
        "questionInput"
    );

const askButton =
    document.getElementById(
        "askButton"
    );

const loadingCard =
    document.getElementById(
        "loadingCard"
    );

const selectedDocumentLabel =
    document.getElementById(
        "selectedDocumentLabel"
    );

const chatContainer =
    document.getElementById(
        "chatContainer"
    );

const clearChatButton =
    document.getElementById(
        "clearChatButton"
    );


let currentFile = null;

let isUploading = false;

let isGenerating = false;

let isDeleting = false;


// =======================================================
// FILE SELECTION
// =======================================================

chooseFileButton.addEventListener(
    "click",
    (event) => {

        event.stopPropagation();

        if (
            isUploading ||
            isDeleting
        ) {
            return;
        }

        fileInput.click();
    }
);


uploadArea.addEventListener(
    "click",
    () => {

        if (
            isUploading ||
            isDeleting
        ) {
            return;
        }

        fileInput.click();
    }
);


fileInput.addEventListener(
    "change",
    () => {

        if (
            fileInput.files.length > 0
        ) {

            setSelectedFile(
                fileInput.files[0]
            );
        }
    }
);


function setSelectedFile(
    file
) {

    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        currentFile = null;

        selectedFile.textContent =
            "";

        showUploadError(
            "Please select a PDF file."
        );

        updateControlStates();

        return;
    }


    currentFile =
        file;


    selectedFile.textContent =
        file.name;


    uploadStatus.textContent =
        "";


    uploadStatus.className =
        "status-message";


    updateControlStates();
}


// =======================================================
// DRAG AND DROP
// =======================================================

uploadArea.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();


        if (
            !isUploading &&
            !isDeleting
        ) {

            uploadArea.classList.add(
                "drag-active"
            );
        }
    }
);


uploadArea.addEventListener(
    "dragleave",
    () => {

        uploadArea.classList.remove(
            "drag-active"
        );
    }
);


uploadArea.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();


        uploadArea.classList.remove(
            "drag-active"
        );


        if (
            isUploading ||
            isDeleting
        ) {

            return;
        }


        const file =
            event.dataTransfer.files[0];


        if (!file) {
            return;
        }


        setSelectedFile(
            file
        );
    }
);


// =======================================================
// UPLOAD DOCUMENT
// =======================================================

uploadButton.addEventListener(
    "click",
    uploadDocument
);


async function uploadDocument() {

    if (
        !currentFile ||
        isUploading
    ) {

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        currentFile
    );


    setUploadLoading(
        true
    );


    uploadStatus.className =
        "status-message";


    uploadStatus.textContent =
        "Extracting text, generating embeddings and indexing document...";


    try {

        const response =
            await fetch(
                "/upload",
                {
                    method:
                        "POST",

                    body:
                        formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Upload failed."
            );
        }


        uploadStatus.className =
            "status-message success";


        uploadStatus.textContent =
            `Indexed successfully • ${data.chunks_created} chunks • OCR pages: ${data.ocr_pages}`;


        currentFile =
            null;


        fileInput.value =
            "";


        selectedFile.textContent =
            "";


        await loadDocuments(
            data.document_name
        );

    }

    catch (error) {

        showUploadError(
            error.message
        );
    }

    finally {

        setUploadLoading(
            false
        );
    }
}


function setUploadLoading(
    loading
) {

    isUploading =
        loading;


    if (loading) {

        uploadButton.textContent =
            "Processing...";


        uploadArea.classList.add(
            "processing"
        );

    }

    else {

        uploadButton.textContent =
            "Upload & Index";


        uploadArea.classList.remove(
            "processing"
        );
    }


    updateControlStates();
}


function showUploadError(
    message
) {

    uploadStatus.className =
        "status-message error";


    uploadStatus.textContent =
        message;
}


// =======================================================
// LOAD DOCUMENTS
// =======================================================

async function loadDocuments(
    selectedDocument = null
) {

    documentSelect.disabled =
        true;


    refreshDocuments.disabled =
        true;


    documentSelect.innerHTML =
        `
        <option value="">
            Loading documents...
        </option>
        `;


    try {

        const response =
            await fetch(
                "/documents"
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to load documents."
            );
        }


        documentSelect.innerHTML =
            "";


        if (
            !data.documents ||
            data.documents.length === 0
        ) {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                "";


            option.textContent =
                "No documents available";


            documentSelect.appendChild(
                option
            );


            updateSelectedDocumentLabel();

            return;
        }


        const defaultOption =
            document.createElement(
                "option"
            );


        defaultOption.value =
            "";


        defaultOption.textContent =
            "Select a document";


        documentSelect.appendChild(
            defaultOption
        );


        data.documents.forEach(
            documentName => {

                const option =
                    document.createElement(
                        "option"
                    );


                option.value =
                    documentName;


                option.textContent =
                    documentName;


                documentSelect.appendChild(
                    option
                );
            }
        );


        if (
            selectedDocument &&
            data.documents.includes(
                selectedDocument
            )
        ) {

            documentSelect.value =
                selectedDocument;
        }


        updateSelectedDocumentLabel();

    }

    catch (error) {

        documentSelect.innerHTML =
            `
            <option value="">
                Failed to load documents
            </option>
            `;


        documentStatus.className =
            "status-message error";


        documentStatus.textContent =
            error.message;

    }

    finally {

        documentSelect.disabled =
            false;


        refreshDocuments.disabled =
            false;


        updateControlStates();
    }
}


// =======================================================
// REFRESH DOCUMENTS
// =======================================================

refreshDocuments.addEventListener(
    "click",
    async () => {

        if (
            isGenerating ||
            isDeleting
        ) {

            return;
        }


        documentStatus.textContent =
            "";


        const currentDocument =
            documentSelect.value;


        await loadDocuments(
            currentDocument
        );
    }
);


// =======================================================
// DOCUMENT SELECTION
// =======================================================

documentSelect.addEventListener(
    "change",
    () => {

        documentStatus.textContent =
            "";


        updateSelectedDocumentLabel();

        updateControlStates();
    }
);


function updateSelectedDocumentLabel() {

    const documentName =
        documentSelect.value;


    if (documentName) {

        selectedDocumentLabel.textContent =
            `Selected: ${documentName}`;

    }

    else {

        selectedDocumentLabel.textContent =
            "No document selected";
    }
}


// =======================================================
// DELETE DOCUMENT
// =======================================================

deleteDocumentButton.addEventListener(
    "click",
    deleteSelectedDocument
);


async function deleteSelectedDocument() {

    const documentName =
        documentSelect.value;


    if (
        !documentName ||
        isDeleting ||
        isGenerating
    ) {

        return;
    }


    const confirmed =
        window.confirm(
            `Delete "${documentName}"?\n\nThis will remove the PDF, processed text and ChromaDB embeddings.`
        );


    if (!confirmed) {

        return;
    }


    isDeleting =
        true;


    deleteDocumentButton.textContent =
        "Deleting...";


    documentStatus.className =
        "status-message";


    documentStatus.textContent =
        "Deleting document...";


    updateControlStates();


    try {

        const response =
            await fetch(
                `/documents/${encodeURIComponent(documentName)}`,
                {
                    method:
                        "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to delete document."
            );
        }


        documentStatus.className =
            "status-message success";


        documentStatus.textContent =
            `Deleted "${documentName}" successfully.`;


        clearChat();


        await loadDocuments();


    }

    catch (error) {

        documentStatus.className =
            "status-message error";


        documentStatus.textContent =
            error.message;

    }

    finally {

        isDeleting =
            false;


        deleteDocumentButton.textContent =
            "Delete";


        updateControlStates();
    }
}


// =======================================================
// ASK QUESTION
// =======================================================

askButton.addEventListener(
    "click",
    askQuestion
);


questionInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();


            if (!isGenerating) {

                askQuestion();
            }
        }
    }
);


questionInput.addEventListener(
    "input",
    updateControlStates
);


async function askQuestion() {

    const question =
        questionInput.value.trim();


    const documentName =
        documentSelect.value;


    if (isGenerating) {

        return;
    }


    if (!documentName) {

        showChatMessage(
            "assistant",
            "Please select a document first."
        );

        return;
    }


    if (!question) {

        showChatMessage(
            "assistant",
            "Please enter a question."
        );

        return;
    }


    removeChatPlaceholder();


    showChatMessage(
        "user",
        question
    );


    questionInput.value =
        "";


    setGeneratingState(
        true
    );


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            {
                                question:
                                    question,

                                document_name:
                                    documentName
                            }
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to generate answer."
            );
        }


        showChatMessage(
            "assistant",
            data.answer
        );

    }

    catch (error) {

        showChatMessage(
            "assistant",
            `Error: ${error.message}`
        );

    }

    finally {

        setGeneratingState(
            false
        );


        questionInput.focus();
    }
}


// =======================================================
// CHAT MESSAGE
// =======================================================

function showChatMessage(
    role,
    message
) {

    removeChatPlaceholder();


    const messageWrapper =
        document.createElement(
            "div"
        );


    messageWrapper.classList.add(
        "chat-message",
        role
    );


    const messageBubble =
        document.createElement(
            "div"
        );


    messageBubble.classList.add(
        "message-bubble"
    );


    const messageLabel =
        document.createElement(
            "div"
        );


    messageLabel.classList.add(
        "message-label"
    );


    messageLabel.textContent =
        role === "user"
            ? "You"
            : "AI Assistant";


    const messageText =
        document.createElement(
            "p"
        );


    messageText.textContent =
        message;


    messageBubble.appendChild(
        messageLabel
    );


    messageBubble.appendChild(
        messageText
    );


    messageWrapper.appendChild(
        messageBubble
    );


    chatContainer.appendChild(
        messageWrapper
    );


    chatContainer.scrollTop =
        chatContainer.scrollHeight;
}


// =======================================================
// GENERATING STATE
// =======================================================

function setGeneratingState(
    generating
) {

    isGenerating =
        generating;


    if (generating) {

        loadingCard.classList.remove(
            "hidden"
        );


        askButton.textContent =
            "Thinking...";

    }

    else {

        loadingCard.classList.add(
            "hidden"
        );


        askButton.textContent =
            "Ask AI";
    }


    updateControlStates();
}


// =======================================================
// CONTROL STATES
// =======================================================

function updateControlStates() {

    const hasDocument =
        Boolean(
            documentSelect.value
        );


    const hasQuestion =
        Boolean(
            questionInput.value.trim()
        );


    uploadButton.disabled =
        (
            !currentFile ||
            isUploading ||
            isGenerating ||
            isDeleting
        );


    chooseFileButton.disabled =
        (
            isUploading ||
            isGenerating ||
            isDeleting
        );


    fileInput.disabled =
        (
            isUploading ||
            isGenerating ||
            isDeleting
        );


    askButton.disabled =
        (
            !hasDocument ||
            !hasQuestion ||
            isGenerating ||
            isUploading ||
            isDeleting
        );


    deleteDocumentButton.disabled =
        (
            !hasDocument ||
            isGenerating ||
            isUploading ||
            isDeleting
        );


    documentSelect.disabled =
        (
            isGenerating ||
            isUploading ||
            isDeleting
        );


    refreshDocuments.disabled =
        (
            isGenerating ||
            isUploading ||
            isDeleting
        );


    clearChatButton.disabled =
        (
            isGenerating ||
            isDeleting
        );


    questionInput.disabled =
        (
            isGenerating ||
            isDeleting
        );
}


// =======================================================
// CLEAR CHAT
// =======================================================

clearChatButton.addEventListener(
    "click",
    clearChat
);


function clearChat() {

    if (isGenerating) {

        return;
    }


    chatContainer.innerHTML =
        `
        <div
            class="chat-placeholder"
            id="chatPlaceholder"
        >

            <div class="assistant-avatar">
                AI
            </div>

            <h3>
                Start a conversation
            </h3>

            <p>
                Select a document and ask a question.
                Your conversation will appear here.
            </p>

        </div>
        `;


    questionInput.value =
        "";


    updateControlStates();


    if (!questionInput.disabled) {

        questionInput.focus();
    }
}


function removeChatPlaceholder() {

    const placeholder =
        document.getElementById(
            "chatPlaceholder"
        );


    if (placeholder) {

        placeholder.remove();
    }
}


// =======================================================
// INITIAL LOAD
// =======================================================

loadDocuments();