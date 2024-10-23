const dropArea = document.querySelector("#drop-area");
/** @type {HTMLInputElement} */
const fileInput = document.querySelector("#file-input");
const fileListContainer = document.querySelector("#file-list-container");

/**
 * @param {FileList} files
 */
function handleFileAdd(files) {
  for (const file of files) {
    if (!isValidFileType(file.type)) continue;

    const fileItem = document.createElement("div");
    fileItem.classList.add("not-ready");
    fileItem.textContent = `${file.name}`;
    fileListContainer.appendChild(fileItem);

    const reader = new FileReader();
    reader.readAsArrayBuffer(file);

    reader.addEventListener("loadend", (e) => {
      fileItem.classList.remove("not-ready");
      fileItem.classList.add("ready");
      // considering we used readAsArrayBuffer above, and it's not null in this callback, cast to ArrayBuffer
      const fileContent = /** @type {ArrayBuffer} */ (e.target.result);

      fileItem.addEventListener(
        "click",
        async () => {
          fileItem.classList.add("upload-in-progress");
          const success = await convertFile(file.name, fileContent);
          fileItem.classList.remove("upload-in-progress");
          fileItem.classList.add(success ? "success" : "error");
        },
        { once: true },
      );
    });
  }
}

/**
 * @param {string} fileName
 * @param {ArrayBuffer} fileContent
 * @returns boolean
 */
async function convertFile(fileName, fileContent) {
  const req = new Request("/upload", {
    method: "PUT",
    body: fileContent,
  });
  try {
    const resp = await fetch(req);
    if (!resp.ok) {
      console.log(resp.status);
      return false;
    }
    const blob = await resp.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    // create fake link and initiate download
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = fileName;
    a.click();
    return true;
  } catch (exc) {
    console.log(exc);
    return false;
  }
}

/**
 * @param {string} type
 * @returns boolean
 */
function isValidFileType(type) {
  const allowedTypes = ["application/vnd.oasis.opendocument.text"];
  return allowedTypes.includes(type);
}

dropArea.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  handleFileAdd(fileInput.files);
});

dropArea.addEventListener("drop", (/** @type {DragEvent} */ ev) => {
  preventDefaults(ev);
  dropArea.classList.remove("drag-over", "drag-reject");
  handleFileAdd(ev.dataTransfer.files);
});

dropArea.addEventListener("dragover", (/** @type {DragEvent} */ ev) => {
  preventDefaults(ev);
  /** @type {boolean} */
  let allow = false;
  if (ev.dataTransfer !== null) {
    // if there's at least one allowed file, then fine, we'll filter the rest later
    allow = Array.prototype.some.call(
      ev.dataTransfer.items,
      (/** @type {DataTransferItem}*/ item) => {
        return isValidFileType(item.type) && item.kind === "file";
      },
    );
  }

  if (allow) {
    dropArea.classList.add("drag-over");
    ev.dataTransfer.dropEffect = "copy";
  } else {
    dropArea.classList.add("drag-reject");
    ev.dataTransfer.dropEffect = "none";
  }
});

dropArea.addEventListener("dragleave", (ev) => {
  preventDefaults(ev);
  dropArea.classList.remove("drag-over", "drag-reject");
});

dropArea.addEventListener("dragenter", preventDefaults);

/**
 * Help popup dialog
 */
/** @type {HTMLDialogElement} */
const dialog = document.querySelector("#help-dialog");
const showButton = document.querySelector("#help-fab>button");
const closeButton = document.querySelector("#help-dialog button");

showButton.addEventListener("click", () => {
  dialog.showModal();
});

closeButton.addEventListener("click", () => {
  dialog.close();
});

dialog.addEventListener("click", () => {
  dialog.close();
});

/** Keyboard shortcuts */
document.addEventListener("keydown", function (ev) {
  if (ev.key === "?") {
    preventDefaults(ev);
    dialog.showModal();
    return;
  }
  if (ev.key === "o") {
    preventDefaults(ev);
    fileInput.click();
    return;
  }
});

/**
 * Service Worker to enable offline use
 */
if ("serviceWorker" in navigator) {
  try {
    const registration = await navigator.serviceWorker.register("/sw.js", {
      scope: "/",
    });
    if (registration.installing) {
      console.log("Service worker for offline use - installing");
    } else if (registration.waiting) {
      console.log("Service worker for offline use - installed");
    } else if (registration.active) {
      console.log("Service worker for offline use - active");
    }
  } catch (error) {
    console.error(
      `Service worker for offline use - Registration failed with ${error}`,
    );
  }
}

/**
 * Utility function to prevent default browser behavior
 * @param {Event} ev
 */
function preventDefaults(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  return false;
}

// prevent droping on the html body to avoid mis-drops
document.body.addEventListener("dragstart", preventDefaults);
document.body.addEventListener("dragenter", preventDefaults);
document.body.addEventListener("dragover", preventDefaults);
document.body.addEventListener("drop", preventDefaults);

// this is an ES module
export {};
