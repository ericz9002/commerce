export function delete_notification(event){
    const notification = event.target.parentElement
    console.log('notification is', notification)
    notification.style.animationPlayState = 'running'
    notification.addEventListener('animationend', ()=>{
        notification.remove()
    })
}