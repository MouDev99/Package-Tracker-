document.addEventListener("DOMContentLoaded", () => {

    user_info = document.querySelector(".user_info")

    profile_icon = document.querySelector(".profile img")
    profile_icon.addEventListener("click", (e) => {
        if (user_info.classList.value.includes("hidden")) {
            e.stopPropagation()
        }
        user_info.classList.remove("hidden")

        document.addEventListener("click", () => {
            user_info.classList.add("hidden")
        })

        user_info.addEventListener("click", (e) => e.stopPropagation() )
    })
})
