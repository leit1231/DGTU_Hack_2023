document.addEventListener('DOMContentLoaded', function(){
    const messagesCont = document.querySelector("#messages_container")
    const messagesInp = document.querySelector("[name=message_input]")
    const SenMSG = document.querySelector("[name=send_message_button]")

    let websocketClient = new WebSocket('ws://localhost:12345');
    websocketClient.onopen = () => {
        console.log('asddsfgdsfgad');
        SenMSG.onclick = () => {
            websocketClient.send(messagesInp.value);
            messagesInp.value = '';

        };

    };
    console.log('asdad');
    websocketClient.onmessage = (msg) => {
    const new_msg = document.createElement('div');
    new_msg.innerHTML = msg.data;
    messages_container.appendChild(new_msg);


    };

}, false);