
const openHamburger = document.getElementById('openHamburger') 


const closeHamburger = document.getElementById('closeHamburger') 

const hamburgerMenu = document.getElementById('hamburgerMenu')

openHamburger.addEventListener("click",()=>{
    hamburgerMenu.classList.remove('hidden') 
    hamburgerMenu.classList.add('flex') 
    openHamburger.classList.add('hidden')
}) 

closeHamburger.addEventListener("click",()=>{
    hamburgerMenu.classList.remove('flex') 
    hamburgerMenu.classList.add('hidden') 
    openHamburger.classList.remove('hidden')
    openHamburger.classList.add('flex')
}) 

const mdScreenSize = window.matchMedia("(min-width: 768px)")

function autoCloseHamburger(screenSize) {
    if (screenSize.matches) {
        hamburgerMenu.classList.remove('flex') 
        hamburgerMenu.classList.add('hidden') 
        openHamburger.classList.remove('hidden')
        openHamburger.classList.add('flex')
    } 
  }
  
mdScreenSize.addEventListener("change", () => {
    autoCloseHamburger(mdScreenSize)
});