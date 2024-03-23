function hashSha256(string) {
    const utf8 = new TextEncoder().encode(string);

    return crypto.subtle.digest("SHA-256", utf8).then(hashBuffer => {
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray
            .map(bytes => bytes.toString(16).padStart(2, "0"))
            .join('');

        return hashHex
    })
}

document.addEventListener("DOMContentLoaded", e => {
    const loginElement = document.querySelector("#login");
    const passwordElement = document.querySelector("#password");
    const buttonSend = document.querySelector("#sendButton");

    loginElement.addEventListener("keyup", e => {
        if (e.key === "Enter") {
            buttonSend.click();
        }
    })

    passwordElement.addEventListener("keyup", e => {
        if (e.key === "Enter") {
            buttonSend.click();
        }
    })

    buttonSend.addEventListener("click", e => {
        hashSha256(passwordElement.value).then(hex => {
            fetch ("/check_login_credentials", {
                method: "POST",
                body: `{"passwordHash": "${hex}", "login": "${loginElement.value}"}`,
            }).then(response => {
                response.text().then(text => {
                    if (text === "TRUE") {
                        buttonSend.textContent = "Успешно!";
                        window.location.replace("/admin_panel");
                    } else {
                        buttonSend.textContent = "Пользователь не найден";
                    }
                })
            })
        })
    })
})