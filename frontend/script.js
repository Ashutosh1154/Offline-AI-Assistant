const fileInput =
    document.getElementById("fileInput");

const chooseFileButton =
    document.getElementById("chooseFileButton");

const uploadButton =
    document.getElementById("uploadButton");

const uploadArea =
    document.getElementById("uploadArea");

const selectedFile =
    document.getElementById("selectedFile");

const uploadStatus =
    document.getElementById("uploadStatus");

const documentSelect =
    document.getElementById("documentSelect");

const refreshDocuments =
    document.getElementById("refreshDocuments");

const questionInput =
    document.getElementById("questionInput");

const askButton =
    document.getElementById("askButton");

const chatContainer =
    document.getElementById("chatContainer");

const chatPlaceholder =
    document.getElementById("chatPlaceholder");

const loadingCard =
    document.getElementById("loadingCard");

const selectedDocumentLabel =
    document.getElementById("selectedDocumentLabel");


let currentFile = null;


chooseFileButton.addEventListener(
    "click",
    (event) => {

        event.stopPropagation();

        fileInput.click();
    }
);


uploadArea.addEventListener(
    "click",
    () => {

        fileInput.click();
    }
);


fileInput.addEventListener(
    "change",
    () => {

        if (fileInput.files.length > 0) {

            currentFile =
                fileInput.files[0];

            selectedFile.textContent =
                currentFile.name;

            uploadButton.disabled = false;
        }

    }
);


uploadArea.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        uploadArea.classList.add(
            "drag-active"
        );
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

        const file =
            event.dataTransfer.files[0];

        if (!file) {
            return;
        }

        currentFile = file;

        selectedFile.textContent =
            file.name;

        uploadButton.disabled = false;
    }
);


uploadButton.addEventListener(
    "click",
    uploadDocument
);


async function uploadDocument() {

    if (!currentFile) {
        return;
    }

    if (
        !currentFile.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        showUploadError(
            "Please select a PDF file."
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        currentFile
    );

    uploadButton.disabled = true;

    uploadButton.textContent =
        "Processing...";

    uploadStatus.className =
        "status-message";

    uploadStatus.textContent =
        "Extracting text, generating embeddings and indexing document...";

    try {

        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
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

        uploadButton.disabled = false;

        uploadButton.textContent =
            "Upload & Index";
    }
}


function showUploadError(message) {

    uploadStatus.className =
        "status-message error";

    uploadStatus.textContent =
        message;
}


async function loadDocuments(
    selectedDocument = null
) {

    documentSelect.innerHTML =
        `<option value="">
            Loading documents...
        </option>`;

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

        documentSelect.innerHTML = "";

        if (
            !data.documents ||
            data.documents.length === 0
        ) {

            documentSelect.innerHTML =
                `<option value="">
                    No documents available
                </option>`;

            return;
        }

        const defaultOption =
            document.createElement(
                "option"
            );

        defaultOption.value = "";

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


        if (selectedDocument) {

            documentSelect.value =
                selectedDocument;

            updateSelectedDocumentLabel();
        }

    }

    catch (error) {

        documentSelect.innerHTML =
            `<option value="">
                Failed to load documents
            </option>`;

        console.error(error);
    }
}


refreshDocuments.addEventListener(
    "click",
    () => {

        loadDocuments();
    }
);


documentSelect.addEventListener(
    "change",
    updateSelectedDocumentLabel
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

            askQuestion();
        }
    }
);


async function askQuestion() {

    const question =
        questionInput.value.trim();

    const documentName =
        documentSelect.value;


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


    if (chatPlaceholder) {

        chatPlaceholder.remove();
    }


    showChatMessage(
        "user",
        question
    );


    questionInput.value = "";


    loadingCard.classList.remove(
        "hidden"
    );

    askButton.disabled = true;

    askButton.textContent =
        "Thinking...";


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
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

        loadingCard.classList.add(
            "hidden"
        );

        askButton.disabled = false;

        askButton.textContent =
            "Ask AI";

        questionInput.focus();
    }
}

function showChatMessage(
    role,
    message
) {

    const messageWrapper =
        document.createElement("div");

    messageWrapper.classList.add(
        "chat-message",
        role
    );


    const messageBubble =
        document.createElement("div");

    messageBubble.classList.add(
        "message-bubble"
    );


    const messageLabel =
        document.createElement("div");

    messageLabel.classList.add(
        "message-label"
    );


    if (role === "user") {

        messageLabel.textContent =
            "You";

    }

    else {

        messageLabel.textContent =
            "AI Assistant";
    }


    const messageText =
        document.createElement("p");

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

function escapeHtml(text) {

    const element =
        document.createElement(
            "div"
        );

    element.textContent = text;

    return element.innerHTML;
}


loadDocuments();
