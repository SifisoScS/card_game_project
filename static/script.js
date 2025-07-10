document.addEventListener('DOMContentLoaded', () => {
    // Card Selection Modal Logic
    const modal = document.getElementById('card-modal');
    let currentSlot = null;

    document.querySelectorAll('.card-slot').forEach(slot => {
        slot.addEventListener('click', () => {
            currentSlot = slot;
            modal.style.display = 'block';
        });
    });

    document.querySelector('.close-modal').addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Card Selection
    document.querySelectorAll('.card-option').forEach(option => {
        option.addEventListener('click', () => {
            const cardValue = option.getAttribute('data-value');
            const select = currentSlot.querySelector('select');
            select.value = cardValue;
            
            // Update visual
            currentSlot.innerHTML = `
                <div class="card-face ${cardValue[1].toLowerCase()}">
                    <span class="card-value">${cardValue[0]}</span>
                    <span class="card-suit">
                        ${cardValue[1] === 'H' ? '♥' : 
                         cardValue[1] === 'D' ? '♦' :
                         cardValue[1] === 'C' ? '♣' : '♠'}
                    </span>
                </div>
            `;
            modal.style.display = 'none';
        });
    });

    // Add Player Button
    document.getElementById('add-player').addEventListener('click', () => {
        const container = document.getElementById('players-container');
        const playerCount = container.children.length + 1;
        
        if (playerCount > 4) {
            alert('Maximum 4 players allowed!');
            return;
        }

        const newPlayer = document.createElement('div');
        newPlayer.className = 'player-card';
        newPlayer.innerHTML = `
            <h3>👤 Player ${playerCount}</h3>
            <input type="text" name="player${playerCount}_name" placeholder="Name">
            <div class="hand-of-cards">
                ${Array(5).fill().map((_, i) => `
                <div class="card-slot" data-player="${playerCount}" data-slot="${i}">
                    <div class="card-back">🂠</div>
                    <select name="player${playerCount}_card${i}" class="hidden-select">
                        <option value="">Select</option>
                        ${['A','2','3','4','5','6','7','8','9','10','J','Q','K'].map(value => 
                            ['H','D','C','S'].map(suit => 
                                `<option value="${value}${suit}">${value}${suit}</option>`
                            ).join('')
                        ).join('')}
                    </select>
                </div>
                `).join('')}
            </div>
        `;
        container.appendChild(newPlayer);
    });
});