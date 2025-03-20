// Function to initialize bottom bar behavior
function initBottomBar() {
    console.log("Initializing bottom bar");
    const bottomBar = $('.bottom-bar');
    
    if (bottomBar.length === 0) {
        console.error("Bottom bar not found");
        return;
    }
    
    // Add hover area to make interaction easier
    if (bottomBar.find('.hover-area').length === 0) {
        bottomBar.append('<div class="hover-area"></div>');
    }
    
    // Expand on hover
    bottomBar.off('mouseenter').on('mouseenter', function() {
        console.log("Mouse entered bottom bar");
        $(this).addClass('expanded');
    });
    
    // Collapse when mouse leaves
    bottomBar.off('mouseleave').on('mouseleave', function() {
        console.log("Mouse left bottom bar");
        $(this).removeClass('expanded');
    });
    
    // Prevent collapse when interacting with controls
    bottomBar.find('button').off('focus').on('focus', function() {
        console.log("Button focused");
        $(this).closest('.bottom-bar').addClass('expanded');
    });
    
    // Initial expansion to show it's working
    setTimeout(function() {
        bottomBar.addClass('expanded');
        setTimeout(function() {
            bottomBar.removeClass('expanded');
        }, 1000);
    }, 500);
    
    console.log("Bottom bar initialization complete");
}

// Initialize on document ready - this is a fallback
$(document).ready(function() {
    // This will be called from the index.html after the bottom bar is loaded
    console.log("Bottom bar JS loaded");
});
