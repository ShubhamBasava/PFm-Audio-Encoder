function scrapeTitlesAndSave() {
    try {
        const selector = 'h2.mb-1.max-w-96.truncate.p-0.text-sm.font-normal';
        const elements = document.querySelectorAll(selector);

        if (elements.length === 0) {
            console.log('No elements found with the specified selector.');
            return;
        }        

        const titles = [];
        elements.forEach((element, index) => {
            let title = element.innerText.trim();
            if (!title.startsWith(`Ep ${index + 1}`)) {
                title = `Ep ${index + 1} ${title}`;
            }
            titles.push(title);
        });

        if (titles.length === 0) {
            console.log('No titles found.');
            return;
        }

        const jsonData = JSON.stringify(titles, null, 2);
        
        // Save the JSON data as a file named chapters.json
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'chapters.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
       
        console.log('Chapters data saved as chapters.json');
    } catch (error) {
        console.error('An error occurred while scraping titles:', error);
    }
}

scrapeTitlesAndSave();
