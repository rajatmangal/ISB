
document.getElementById("topicName").addEventListener('click', function() {
    document.getElementById("textForm").style.display = "inline-block";
    document.getElementById("descriptionForm").style.display = "none";
})


document.getElementById("topicDescription").addEventListener('click', function() {
    document.getElementById("textForm").style.display = "none";
    document.getElementById("descriptionForm").style.display = "inline-block";
})