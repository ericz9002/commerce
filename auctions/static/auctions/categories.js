document.addEventListener('DOMContentLoaded', () =>{
    const form = document.querySelector('#category-form');
    const select = form.querySelector('#category-select');
    const error_ele = document.querySelector('.error');
    const listings = document.querySelector('#listings');
    form.addEventListener('submit', (event)=>{
        const selectValue = select.options[select.selectedIndex].text;
        event.preventDefault();
        listings.innerHTML = "";
        error_ele.innerText = "";
        const request = new Request(`category-data/${selectValue}`, {
            method: "GET",
        })
        fetch(request)
        .then((response) =>{
            console.log('response.status is ', response.status);
            if(response.status != 200){
                response.json()
                .then((data) =>{
                    error_ele.innerText = data.error;
                })
            }
            else{
                console.log('response is ', response);
                response.text()
                .then((data) =>{
                    listings.innerHTML = data;
                })
            }
        })
        .catch((error) =>{
            error_ele.innerText = error;
        })
    })
    form.addEventListener('change', (event)=>{
        form.requestSubmit();
    })
})