function navclick(focus) {
    const element = document.querySelectorAll(".nav-item")
    element.forEach(function (item) {
        let comparacao = item.getElementsByTagName("a")[0].href
        if (item.style.borderBottom !== "") {
            item.style.borderBottom = ""
        }
        if (comparacao === focus.getElementsByTagName("a")[0].href) {
            item.style.borderBottom = "3px solid orange"
        }
    })
}

function collapse() {
    const element = document.getElementById("mobile_menu")
    const icon = document.getElementById("mobile_btn")
    if (element.style.left === "-100vw" || element.style.left === "") {
        element.style.left = "0"
        icon.className = "fa-solid fa-xmark"
    } else {
        element.style.left = "-100vw"
        icon.className = "fa-solid fa-bars"
    }
}

function effect() {
    const scroll = window.scrollY
    const element = document.querySelectorAll(".nav-item")
    if (scroll > 92) {
        document.getElementsByTagName("header")[0].style.backgroundColor = "var(--color-primary-1)"
    } else {
        document.getElementsByTagName("header")[0].style.backgroundColor = "transparent"
    }
    element.forEach(function (item) {
        let focus = item.getElementsByTagName("a")[0].href
        let position = document.getElementById(focus.substring(focus.search(/#/)+1))
        if (scroll >= position.getBoundingClientRect().top) {
            navclick(item)
        }
    })
}

function formulario(focus) {
    const element = document.getElementById(focus)
    const outhers = document.querySelectorAll(".page")
    const header = document.getElementsByTagName("header")[0]
    const body = document.getElementsByTagName("body")[0]
    const icons = document.querySelectorAll(".nav-buttons")[0].querySelectorAll(".fa-solid")

    const voltar = document.getElementById("voltar")
    outhers.forEach(function (item) {
        item.style.display = "none"
    })


    switch (focus) {
        case 'cadastro':
            voltar.onclick = function() {formulario('login')}
            break;
        case 'esqueci_senha':
            voltar.onclick = function() {formulario('login')}
            break;
        default:
            voltar.onclick = function() {formulario()}
    }

    if (focus == null || focus === "") {
            body.style.overflowY = ""
            if (window.innerWidth <= 1080) {
                icons.forEach(function (i) {
                i.style.display = "block"
                })
                voltar.style.display = "none"
                header.style.backgroundColor = "transparent"
            }
    } else {
        if (element.style.display === null || element.style.display === "none") {
            element.style.display = "flex"
            if (window.innerWidth <= 1080) {
                icons.forEach(function (i) {
                    i.style.display = "none"
                })
                voltar.style.display = "block"
                header.style.backgroundColor = "white"
            }
        }
        body.style.overflowY = "hidden"
    }
}