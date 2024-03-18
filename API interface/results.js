document.addEventListener("DOMContentLoaded", function() {
    const results = JSON.parse(localStorage.getItem('results')); // Retrieve the data from local storage
    const listElement = document.getElementById('giftList');

    // Check if results exist
    if (results && results.length > 0) {
        results.forEach(item => {
            // Create a list item for the main description
            const descriptionItem = document.createElement('li');
            descriptionItem.innerHTML = `<strong>${item.description}</strong>`;
            listElement.appendChild(descriptionItem);

            // Create a sublist for agent items
            const agentList = document.createElement('ul');

            item.agent_items.forEach(agentItem => {
                const agentListItem = document.createElement('li');
                agentListItem.innerHTML = `
                    <a href="${agentItem.link}" target="_blank">Link</a>, 
                    Price: ${agentItem.price}, 
                    Rating: ${agentItem.rating}
                `;
                agentList.appendChild(agentListItem);
            });

            // Append the sublist to the main list
            listElement.appendChild(agentList);
        });
    } else {
        // If no results, display a message
        listElement.innerHTML = '<li>No items found.</li>';
    }

    localStorage.removeItem('results'); // Clear the results from local storage
});
