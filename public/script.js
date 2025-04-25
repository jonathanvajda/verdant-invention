    async function loadResource() {
      const params = new URLSearchParams(window.location.search);
      const iri = params.get('iri');
      const contentDiv = document.getElementById('content');

      if (!iri) {
        contentDiv.innerHTML = '<h1>No IRI provided.</h1>';
        return;
      }

      try {
        const response = await fetch('data.json');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        const resource = data.find(item => item.iri === iri);

        if (resource) {
          contentDiv.innerHTML = `
            <h1>${resource.label}</h1>
            <p>${resource.description}</p>
          `;
        } else {
          contentDiv.innerHTML = `
            <h1>Resource Not Found</h1>
            <p>We couldn't find a resource matching the IRI you provided.</p>
          `;
        }
      } catch (error) {
        console.error("Error loading data:", error);
        contentDiv.innerHTML = `
          <h1 id="error">Error Loading Resource</h1>
          <p>There was a problem retrieving the resource information. Please try again later.</p>
        `;
      }
    }

    loadResource();
