document.addEventListener('DOMContentLoaded', ()=>{
    function sleep(ms) {
        const start = Date.now();
        while (Date.now() - start < ms) {
            // Busy-waiting: Blocks execution
        }
    }

    const comment_input = document.querySelector('#comment-input');
    const form = document.querySelector('#comment-form');
    const csrf_token = document.querySelector('#comment-form input[name="csrfmiddlewaretoken"]').value;
    //const listing_str = '{{serialized_listing|escapejs}}'.slice(2,-1)
    const listing_str = '{{serialized_listing|escapejs}}';
    console.log(`listing_str is typeof ${typeof listing_str}`);
    console.log(`listing_str is ${listing_str}`);
    const listing = JSON.parse(listing_str);
    console.log(`listing.title is ${listing.title}`);
    console.log(`listing is typeof ${typeof listing}`);
    console.log(`listing is ${listing}`);
    console.log(listing);
    form.addEventListener('submit', (event)=>{
        event.preventDefault();
        console.log('submitted form');
        const request = new Request("{%url 'add_comment' %}", {
            method: "POST",
            headers: {'X-CSRFToken': csrf_token},
            body: JSON.stringify({"comment": comment_input.value, "listing":listing}),
        });
        console.log(`submitting {comment: ${comment_input.value}, csrfmiddlewaretoken: ${csrf_token}}, listing: ${listing}}`);
        fetch(request)
            .then((response) =>{
                console.log(response)
                return response.text()
            })
            .then(data =>  {
                console.log('in then2');
                console.log("data is", data);
                const comments_list = document.querySelector('#comments');
                const new_comment = document.createElement('li')
                new_comment.innerHTML = data;
                new_comment.classList.add('comment');
                comments_list.appendChild(new_comment);
            })
            .catch(error => {
                console.log('in catch');
                console.log(`Error: ${error}`);
            })
        console.log('after fetch');      
    });



    comment_input.addEventListener('keydown', (event)=>{
        if(event.key === 'Enter'){
            event.preventDefault();
            console.log('something');
            form.requestSubmit();
            form.reset();
            comment_input.blur();
        }
    })
})