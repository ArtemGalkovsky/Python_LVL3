var alertTimeout;

function removeErrorIfExists() {
    if (alertTimeout) {
        clearTimeout(alertTimeout)
    }

    const errorElement = document.querySelector(".error")

    if (errorElement) {
        document.body.removeChild(errorElement)
    }
}

function createTextElement(tag, value, placeholder, classes, castleDataElement) {
    const element = document.createElement(tag)
    element.classList.add(...classes)
    element.value = value
    element.placeholder = placeholder

    castleDataElement.appendChild(element)

    return element
}

function changeImageHandler(imageElement, inputElement) {
    inputElement.addEventListener("change", e => {
        const file = inputElement.files[0]

        fetch(`/download_to_temp?name=${file.name}`, {
            method: "POST",
            body: file,   
        }).then(response => {
            response.text().then(text => {
                imageElement.src = text
            }) 
        })
    })
}

function createPreview(url, castleDataElement) {
    const previewContainer = document.createElement("div")
    previewContainer.classList.add("preview_container")

    const previewElement = document.createElement("img")
    previewElement.classList.add("castle_preview", "castle_img")
    previewElement.src = url

    previewContainer.appendChild(previewElement)

    const labelForInput = document.createElement("label")
    labelForInput.textContent = "Заменить изображение"
    labelForInput.classList.add("change_preview_label")

    const changeImageButton = document.createElement("input")
    changeImageButton.type = "file"
    changeImageButton.accept = "image/*"
    changeImageButton.classList.add("change_preview_button")

    labelForInput.appendChild(changeImageButton)
    previewContainer.appendChild(previewElement)
    previewContainer.appendChild(labelForInput)
    castleDataElement.appendChild(previewContainer)

    changeImageHandler(previewElement, changeImageButton)
}

function drawAlbumNavigation() {
    const mainContainer = document.querySelector(".image_container")
    const middleContainers = Array.from(document.querySelectorAll(".album_image_middle_container"))

    middleContainers.forEach((middleContainer, index) => {
        middleContainer.querySelector(".nav_up")?.remove()
        middleContainer.querySelector(".nav_down")?.remove()

        drawNavigation(mainContainer, middleContainer, index, middleContainers.length-1, drawAlbumNavigation)
    })
}

function createAlbumImage(imageUrl, imageContainer) {
    const middleImageContainer = document.createElement("div")
    middleImageContainer.classList.add("album_image_middle_container")

    const imageElement = document.createElement("img")
    imageElement.classList.add("castle_image")
    imageElement.src = STATICFOLDER + "/" + imageUrl
    
    const buttonDeleteImage = document.createElement("button")
    const buttonRestoreImage = document.createElement("button")
    const labelForInput = document.createElement("label")
    labelForInput.textContent = "Заменить изображение"
    labelForInput.classList.add("change_album_image_label")

    buttonDeleteImage.textContent = "Удалить картинку"
    buttonDeleteImage.type = "button"
    buttonDeleteImage.classList.add("button_delete_image")

    buttonDeleteImage.addEventListener("click", e => {
        buttonDeleteImage.style.display = "none"
        imageElement.style.display = "none"
        buttonRestoreImage.style.display = "inline",
        labelForInput.style.display = "none"
        middleImageContainer.classList.add("deleted")
    })

    buttonRestoreImage.textContent = "Восстановить"
    buttonRestoreImage.type = "button"
    buttonRestoreImage.classList.add("button_restore_image")
    buttonRestoreImage.style.display = "none"

    buttonRestoreImage.addEventListener("click", e => {
        buttonDeleteImage.style.display = "inline"
        imageElement.style.display = "inline"
        buttonRestoreImage.style.display = "none"
        labelForInput.style.display = "inline"
        middleImageContainer.classList.remove("deleted")
    })


    const changeImageButton = document.createElement("input")
    changeImageButton.type = "file"
    changeImageButton.accept = "image/*"
    changeImageButton.classList.add("change_album_image")
    

    middleImageContainer.appendChild(imageElement)
    imageContainer.appendChild(middleImageContainer)
    labelForInput.appendChild(changeImageButton)
    middleImageContainer.append(labelForInput)
    middleImageContainer.appendChild(buttonDeleteImage)
    middleImageContainer.appendChild(buttonRestoreImage)
    
    changeImageHandler(imageElement, changeImageButton)
}

function createAlbum(imagesUrls, castleDataElement) {
    const imageContainer = document.createElement("div")
    imageContainer.classList.add("image_container")

    const addImageButton = document.createElement("button")
    addImageButton.type = "button"
    addImageButton.textContent = "Добавить картинку"
    
    addImageButton.addEventListener("click", e => {
        createAlbumImage("", imageContainer)
        drawAlbumNavigation()
    })

    imageContainer.appendChild(addImageButton)

    imagesUrls.forEach(imageUrl => {
        createAlbumImage(imageUrl, imageContainer)
    })

    castleDataElement.appendChild(imageContainer)

    drawAlbumNavigation()
}

function moveElement(element, container, beforeElement) {
    container.insertBefore(element, beforeElement)
}

function drawNavigation(mainContainer, middleContainer, index, maxIndex, drawNavigationFunction) {
    const navigationUp = document.createElement("img")
    const navigationDown = document.createElement("img")

    navigationUp.classList.add("nav_up")
    navigationDown.classList.add("nav_down")

    navigationUp.src = STATICFOLDER + "/" + "files/img/admin_panel/up.png"
    navigationDown.src = STATICFOLDER + "/" + "files/img/admin_panel/down.png"

    if (index == maxIndex) {
        middleContainer.appendChild(navigationUp)
    } else if (index == 0) {
        middleContainer.appendChild(navigationDown)
    } else {
        middleContainer.appendChild(navigationDown)
        middleContainer.appendChild(navigationUp)
    }

    navigationUp.addEventListener("click", e => {
        moveElement(middleContainer, mainContainer, middleContainer.previousSibling)
        drawNavigationFunction()
    })

    navigationDown.addEventListener("click", e => {
        moveElement(middleContainer, mainContainer, middleContainer.nextSibling.nextSibling)
        drawNavigationFunction()
    })
}

function drawParagraphNavigation() {
    const mainContainer = document.querySelector(".paragraph_container")
    const middleContainers = Array.from(document.querySelectorAll(".paragraph_middle_container"))

    middleContainers.forEach((middleContainer, index) => {
        middleContainer.querySelector(".nav_up")?.remove()
        middleContainer.querySelector(".nav_down")?.remove()

        drawNavigation(mainContainer, middleContainer, index, middleContainers.length-1, drawParagraphNavigation)
    })
}

function createParagraph(paragraphText, paragraphContainer) {
    const currentParagraphContainer = document.createElement("div")
    currentParagraphContainer.classList.add("paragraph_middle_container")

    paragraphContainer.appendChild(currentParagraphContainer)
    const paragraphElement = createTextElement("textarea", paragraphText, "Параграф", ["castle_paragraph", "castle_info"], currentParagraphContainer, draggable=true)

    const buttonDeleteParagraph = document.createElement("button")
    const buttonRestoreParagraph = document.createElement("button")
    
    buttonDeleteParagraph.textContent = "Удалить параграф"
    buttonDeleteParagraph.type = "button"
    buttonDeleteParagraph.classList.add("button_delete_paragraph")
    currentParagraphContainer.appendChild(buttonDeleteParagraph)

    buttonDeleteParagraph.addEventListener("click", e => {
        buttonDeleteParagraph.style.display = "none"
        paragraphElement.style.display = "none"
        buttonRestoreParagraph.style.display = "block"
        currentParagraphContainer.classList.add("deleted")
    })

    buttonRestoreParagraph.textContent = "Восстановить"
    buttonRestoreParagraph.type = "button"
    buttonRestoreParagraph.classList.add("button_restore_paragraph")
    buttonRestoreParagraph.style.display = "none"
    currentParagraphContainer.appendChild(buttonRestoreParagraph)

    buttonRestoreParagraph.addEventListener("click", e => {
        buttonDeleteParagraph.style.display = "block"
        paragraphElement.style.display = "block"
        buttonRestoreParagraph.style.display = "none"
        currentParagraphContainer.classList.remove("deleted")
    })
}

function clearCastleData() {
    removeErrorIfExists()

    const mainElement = document.querySelector("main")

    let castleDataElement = document.querySelector(".castle_data")
    castleDataElement.remove()

    castleDataElement = document.createElement("div")
    castleDataElement.classList.add("castle_data")

    mainElement.appendChild(castleDataElement)

    return castleDataElement
}

function renderCastleData(json) {
    removeErrorIfExists()

    const castleDataElement = clearCastleData()
    castleDataElement.dataset.id = json.preview[4]

    createTextElement("input", json.preview[1], "Название замка", ["castle_title", "castle_info"], castleDataElement)
    createTextElement("textarea", json.preview[3], "Описание", ["castle_description", "castle_info"], castleDataElement)
    createPreview(STATICFOLDER + "/" + json.preview[2], castleDataElement)
        
    const paragraphContainer = document.createElement("div")
    paragraphContainer.classList.add("paragraph_container")

    castleDataElement.appendChild(paragraphContainer)
        
    const addParagraphButton = document.createElement("button")
    addParagraphButton.classList.add("add_paragraph_button")
    addParagraphButton.textContent = "Добавить параграф"
    addParagraphButton.type = "button"

    paragraphContainer.appendChild(addParagraphButton)

    addParagraphButton.addEventListener("click", e => {
        createParagraph("", paragraphContainer, true)
        drawParagraphNavigation()
    })

    const paragraphMaxIndex = json.paragraphs.length - 1
    json.paragraphs.forEach((paragraph, index) => {
        createParagraph(paragraph, paragraphContainer, index, paragraphMaxIndex)
    });

    drawParagraphNavigation()

    createAlbum(json.images, castleDataElement)

    const saveButton = document.createElement("button")
    saveButton.textContent = "Сохранить"
    saveButton.type = "button"
    saveButton.classList.add("submit_button")

    saveButton.addEventListener("click", e => {
        const castleId = document.querySelector(".castle_data").dataset.id
        const titleText = document.querySelector(".castle_title").value
        const descriptionText = document.querySelector(".castle_description").value
        const previewImageUrl = document.querySelector(".castle_preview").src
        const paragraphsMiddles = document.querySelectorAll(".paragraph_middle_container")
        let paragraphTexts = Array() 

        paragraphsMiddles.forEach(middleElement => {
            if (!middleElement.classList.contains("deleted")) {
                paragraphTexts.push(middleElement.querySelector(".castle_paragraph").value)
            }
        })

        const imagesMiddles = document.querySelectorAll(".album_image_middle_container")
        let imagesUrls = Array()

        imagesMiddles.forEach(middle => {
            if (!middle.classList.contains("deleted")) {
                imagesUrls.push(decodeURIComponent(middle.querySelector(".castle_image").src))
            }
        })
        
        fetch("/save", {
            method: "POST",
            body: JSON.stringify({
                id: castleId,
                title: titleText,
                description: descriptionText,
                preview: previewImageUrl,
                paragraphs: paragraphTexts,
                images: imagesUrls 
            }),
            headers: {"Content-Type": "application/json",
                      "Accept": "application/json, application/xml, text/plain, text/html, *.*"}
        }).then(response => {
            console.log(response, response.statusText)
            if (response.statusText === "OK") {
                showAlert("Успешно сохранен", "green")
                window.location.reload()
            } else {
                showAlert("Не удалось сохранить файл")
            }
        }).catch(error => {
            showAlert("Ошибка сохранения")
        })
    })

    castleDataElement.appendChild(saveButton)


    const deleteButton = document.createElement("button")
    deleteButton.textContent = "Удалить замок"
    deleteButton.type = "button"
    deleteButton.classList.add("delete_button")

    deleteButton.addEventListener("click", e => {
        const castleId = document.querySelector(".castle_data").dataset.id

        fetch("/delete_castle", {
            method: "POST",
            body: castleId
        }).then(response => {
            if (response.statusText == "OK") {
                showAlert("Безвозвратно удалён!", "green")
                window.location.reload()
            } else {
                showAlert("Что-то пошло не так!")
            }
        })
    })

    castleDataElement.appendChild(deleteButton)
}

function showAlert(message, color="red") {
    removeErrorIfExists()

    const errorElement = document.createElement("div")
    errorElement.classList.add("error")
    errorElement.style = "width: 300px; height: 100px; font-size: 35px; padding: 10px; color: white; border-radius: 10px;"
    errorElement.style.backgroundColor = color
    errorElement.textContent = message
    
    document.body.appendChild(errorElement)

    alertTimeout = setTimeout(() => {
        removeErrorIfExists()
    }, 2000)
}

function addCastle() {
    const container = clearCastleData()
    removeErrorIfExists()

    const castleIdElement = document.createElement("input")
    castleIdElement.classList.add("add_castle_id_input")
    castleIdElement.placeholder = "Название страницы"

    const castleTitleElement = document.createElement("input")
    castleTitleElement.classList.add("add_castle_title_input")
    castleTitleElement.placeholder = "Заголовок"

    const createButton = document.createElement("button")
    createButton.type = "button"
    createButton.classList.add("add_create_button")
    createButton.textContent = "Создать замок"

    container.appendChild(castleIdElement)
    container.appendChild(castleTitleElement)
    container.appendChild(createButton)

    createButton.addEventListener("click", e => {
        const castleIdText = castleIdElement.value
        const titleText = castleTitleElement.value

        if (castleIdText !== "" && titleText != "") {
            fetch("/create_castle", {
                method: "POST",
                body: `{"page": "${castleIdText}", "title": "${titleText}"}`,
                headers: {"Content-Type": "application/json",
                          "Accept": "application/json, application/xml, text/plain, text/html, *.*"}
            }).then(response => {
                if (response.statusText == "OK") {
                    showAlert("Создан!", "green")
                    window.location.reload()
                } else {
                    showAlert("Ошибка создания")
                }
            })
        } else {
            showAlert("Не все данные заполнены")
        }
    })
}

function checkCurrentLocation() {
    let currentLocation = window.location.hash;
        
    if (currentLocation == "#add") {
        addCastle()
    } else if (currentLocation !== "#" && currentLocation !== "") {
        fetch(`/load`, {
            method: "POST",
            body: `${currentLocation.replace("#", "")}`
        }).then(response => {
            response.json().then(json => {
                if ("msg" in json) {
                    showAlert(json.msg)
                } else {
                    renderCastleData(json)
                }
            })
        })
    }
}

document.addEventListener("DOMContentLoaded", e => {
    checkCurrentLocation()

    window.addEventListener("hashchange", e => {
        checkCurrentLocation()
    })
})
