css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
    width: 20%;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://media.istockphoto.com/id/1413286466/vector/chat-bot-icon-robot-virtual-assistant-bot-vector-illustration.jpg?s=612x612&w=0&k=20&c=ZSG3eqGPDJgIgFUIuVxID64uVUF3eqM3LrrDWtaKses=" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''


user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://mir-s3-cdn-cf.behance.net/projects/404/22354754671133.Y3JvcCwxMDI2LDgwMywwLDE1NA.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
