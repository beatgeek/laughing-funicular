// Content Journey Finder - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const planJourneyBtn = document.getElementById('plan-journey-btn');
    const durationInput = document.getElementById('duration');
    const preferencesInput = document.getElementById('preferences');
    const contentTypeSelect = document.getElementById('content-type');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const journeyInfo = document.getElementById('journey-info');
    const contentList = document.getElementById('content-list');

    planJourneyBtn.addEventListener('click', planJourney);

    async function planJourney() {
        const duration = parseInt(durationInput.value);
        const preferences = preferencesInput.value.trim();
        const contentType = contentTypeSelect.value;

        // Validate input
        if (duration < 30) {
            showError('Journey duration must be at least 30 minutes');
            return;
        }

        // Hide results and errors
        resultsDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        loadingDiv.style.display = 'block';

        try {
            const response = await fetch('/api/plan-journey', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    duration: duration,
                    preferences: preferences,
                    content_type: contentType || null
                })
            });

            const data = await response.json();

            if (data.success) {
                displayJourney(data.journey);
            } else {
                showError(data.error || 'An error occurred while planning your journey');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to connect to the server. Please try again.');
        } finally {
            loadingDiv.style.display = 'none';
        }
    }

    function displayJourney(journey) {
        // Display journey summary
        const hours = Math.floor(journey.total_duration / 60);
        const minutes = journey.total_duration % 60;
        const durationText = hours > 0 
            ? `${hours} hour${hours > 1 ? 's' : ''} ${minutes} minutes`
            : `${minutes} minutes`;

        journeyInfo.innerHTML = `
            <p><strong>Total Duration:</strong> ${durationText} (${journey.total_duration} minutes)</p>
            <p><strong>Number of Legs:</strong> ${journey.contents.length}</p>
            <p><strong>Ready for takeoff!</strong> 🛫</p>
        `;

        // Display content list
        contentList.innerHTML = '';
        journey.contents.forEach((content, index) => {
            const contentCard = createContentCard(content, index + 1);
            contentList.appendChild(contentCard);
        });

        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function createContentCard(content, legNumber) {
        const card = document.createElement('div');
        card.className = 'content-card';

        const legDiv = document.createElement('div');
        legDiv.className = 'leg-number';
        legDiv.textContent = legNumber;

        const detailsDiv = document.createElement('div');
        detailsDiv.className = 'content-details';

        const title = document.createElement('h4');
        title.className = 'content-title';
        title.textContent = content.title;

        const metaDiv = document.createElement('div');
        metaDiv.className = 'content-meta';

        // Content type badge
        const typeBadge = document.createElement('span');
        typeBadge.className = 'badge badge-type';
        typeBadge.textContent = content.content_type === 'movie' ? '🎬 Movie' : '📺 TV Show';
        metaDiv.appendChild(typeBadge);

        // Duration badge
        const durationBadge = document.createElement('span');
        durationBadge.className = 'badge badge-duration';
        const hours = Math.floor(content.duration_minutes / 60);
        const mins = content.duration_minutes % 60;
        durationBadge.textContent = hours > 0 
            ? `⏱️ ${hours}h ${mins}m` 
            : `⏱️ ${mins}m`;
        metaDiv.appendChild(durationBadge);

        // Rating badge
        if (content.rating) {
            const ratingBadge = document.createElement('span');
            ratingBadge.className = 'badge badge-rating';
            ratingBadge.textContent = `⭐ ${content.rating}%`;
            metaDiv.appendChild(ratingBadge);
        }

        // Year badge
        if (content.year) {
            const yearBadge = document.createElement('span');
            yearBadge.className = 'badge badge-year';
            yearBadge.textContent = `📅 ${content.year}`;
            metaDiv.appendChild(yearBadge);
        }

        // Genres
        let genresDiv = null;
        if (content.genres && content.genres.length > 0) {
            genresDiv = document.createElement('div');
            genresDiv.className = 'content-genres';
            content.genres.forEach(genre => {
                const genreTag = document.createElement('span');
                genreTag.className = 'genre-tag';
                genreTag.textContent = genre;
                genresDiv.appendChild(genreTag);
            });
        }

        // Description
        let descriptionDiv = null;
        if (content.description) {
            descriptionDiv = document.createElement('p');
            descriptionDiv.className = 'content-description';
            descriptionDiv.textContent = content.description;
        }

        // Assemble the card
        detailsDiv.appendChild(title);
        detailsDiv.appendChild(metaDiv);
        if (genresDiv) detailsDiv.appendChild(genresDiv);
        if (descriptionDiv) detailsDiv.appendChild(descriptionDiv);

        card.appendChild(legDiv);
        card.appendChild(detailsDiv);

        return card;
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
