import {delete_notification} from './delete_notification.js'

document.addEventListener('DOMContentLoaded', ()=>{
    function add_to_watchlist(){
        console.log('this is', this)
        const csrf_token = this.previousElementSibling.value
        const request = new Request("/add_watchlist", {
            method: 'POST',
            headers: {'X-CSRFToken': csrf_token},
            body: JSON.stringify({"listing_id": this.dataset.listing, "listing_creator":this.dataset.user}),
            credentials: "include",
        });
        console.log("request body is", request.body)
        fetch(request)
        .then((response)=>{
            return response.text()
        })
        .then((data)=>{
            let notification = document.createElement('div')
            notification.innerHTML = data
            notification = notification.firstElementChild
            const listing_ele = this.parentElement.parentElement
            const delete_icon = notification.querySelector(".delete-icon")
            delete_icon.addEventListener('click', delete_notification)
            listing_ele.insertAdjacentElement('beforebegin', notification)
            this.classList.replace("add-watchlist", "remove-watchlist")
            this.innerHTML = '<img src= "/static/auctions/red_minus.png" class="icon"> Remove from Watchlist'
            this.removeEventListener('click', add_to_watchlist)
            this.addEventListener('click', remove_from_watchlist)
        })
        .catch((error)=>{
            console.log('error is', error)
        })
    }

    function remove_from_watchlist(){
        const csrf_token = this.previousElementSibling.value
        const request = new Request("/remove_watchlist", {
            method: 'POST',
            headers: {'X-CSRFToken': csrf_token},
            body: JSON.stringify({"listing_id": this.dataset.listing, "listing_creator":this.dataset.user}),
            credentials: "include",
        });
        console.log("request body is", request.body)
        fetch(request)
        .then((response)=>{
            return response.text()
        })
        .then((data)=>{
            let notification = document.createElement('div')
            notification.innerHTML = data
            notification = notification.firstElementChild
            const listing_ele = this.parentElement.parentElement
            const delete_icon = notification.querySelector(".delete-icon")
            delete_icon.addEventListener('click', delete_notification)
            listing_ele.insertAdjacentElement('beforebegin', notification)
            this.classList.replace("remove-watchlist", "add-watchlist")
            this.innerHTML = '<img src= "/static/auctions/green_add.png" class="icon"> Add to Watchlist'
            this.removeEventListener('click', remove_from_watchlist)
            this.addEventListener('click', add_to_watchlist)
        })
        .catch((error)=>{
            console.log('error is', error)
        })
    }


    document.querySelectorAll('.add-watchlist').forEach((button) =>{
        button.addEventListener('click', add_to_watchlist)
    })

    document.querySelectorAll('.remove-watchlist').forEach((button) =>{
        button.addEventListener('click', remove_from_watchlist)
    })
})