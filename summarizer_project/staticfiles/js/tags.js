// JavaScript for handling tags

// Function to add a tag
function addTag(tag) {
    // Create a new span element for the tag
    var tagElement = document.createElement('span');
    tagElement.className = 'tag';
    tagElement.textContent = tag;

    // Add click event listener to remove the tag when clicked
    tagElement.addEventListener('click', function() {
        tagElement.parentNode.removeChild(tagElement); // Remove the tag from DOM
        updateHiddenInput(); // Update the hidden input field
    });

    // Append the tag to the tags container
    document.getElementById('tags-container').appendChild(tagElement);

    // Update the hidden input field
    updateHiddenInput();
}

// Function to update the hidden input field with the tags
function updateHiddenInput() {
    var tags = document.querySelectorAll('.tag');
    var keywordsInput = document.getElementById('keywords');
    var keywords = [];

    // Extract tags text
    tags.forEach(function(tag) {
        keywords.push(tag.textContent);
    });

    // Update hidden input value with comma-separated tags
    keywordsInput.value = keywords.join(',');
}

// Function to handle adding tags when space key is pressed
function handleTags() {
    var keywordsInput = document.getElementById('youtube_url');

    // Add tag when space key is pressed
    keywordsInput.addEventListener('keypress', function(event) {
        if (event.keyCode === 32) { // Check if space key is pressed
            var tag = keywordsInput.value.trim(); // Get the entered text
            if (tag) {
                addTag(tag); // Add the text as a tag
                keywordsInput.value = ''; // Clear the input field
            }
        }
    });
}

// Add tags when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    handleTags();
});
