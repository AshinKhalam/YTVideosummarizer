// JavaScript for handling keywords as bubbles with close icons

// Function to add a keyword bubble
function addKeywordBubble(keyword) {
    // Create a new div for the keyword bubble
    var keywordBubble = document.createElement('div');
    keywordBubble.className = 'keyword-bubble';

    // Add keyword text
    var keywordText = document.createElement('span');
    keywordText.className = 'keyword-text';
    keywordText.textContent = keyword;

    // Add close icon
    var closeIcon = document.createElement('span');
    closeIcon.className = 'close-icon';
    closeIcon.textContent = '×'; // Close icon symbol

    // Add click event listener to remove the keyword bubble when close icon is clicked
    closeIcon.addEventListener('click', function() {
        keywordBubble.remove();
    });

    // Append text and close icon to keyword bubble
    keywordBubble.appendChild(keywordText);
    keywordBubble.appendChild(closeIcon);

    // Append keyword bubble to the keywords container
    document.getElementById('keywords-container').appendChild(keywordBubble);
}

// Function to handle adding keyword bubbles when a keyword is entered
function handleKeywords() {
    var keywordsInput = document.getElementById('keywords');

    // Add keyword bubble when Enter key is pressed
    keywordsInput.addEventListener('keypress', function(event) {
        if (event.keyCode === 13) { // Check if Enter key is pressed
            var keyword = keywordsInput.value.trim(); // Get the entered keyword
            if (keyword) {
                addKeywordBubble(keyword); // Add the keyword as a bubble
                keywordsInput.value = ''; // Clear the input field
            }
        }
    });
}

// Add keyword bubbles when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    handleKeywords();
});
