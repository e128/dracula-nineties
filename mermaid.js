  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@12.0.0/dist/mermaid.esm.min.mjs';
    const mermaidLight = getComputedStyle(document.documentElement).getPropertyValue('--mermaid-scheme').trim() === 'light';
    const mermaidFont = '"Cousine", "Courier New", Courier, monospace';
    const mermaidDark = {
      background:          '#1e1e2e',
      mainBkg:             '#1e1e2e',
      primaryColor:        '#1e1e2e',
      primaryTextColor:    '#ffffff',
      primaryBorderColor:  '#bd93f9',
      lineColor:           '#808080',
      textColor:           '#ffffff',
      secondaryColor:      '#12121a',
      clusterBkg:          '#1e1e2e',
      clusterBorder:       '#666666',
      nodeBorder:          '#bd93f9',
      edgeLabelBackground: '#1e1e2e',
      noteBkgColor:        '#1e1e2e',
      noteTextColor:       '#ffffff',
      noteBorderColor:     '#666666',
      archEdgeColor:       '#808080',
      archGroupBorderColor: '#666666',
      pie1: '#8be9fd', pie2: '#ff79c6', pie3: '#50fa7b', pie4: '#f1fa8c',
      pieSectionTextColor: '#000000',
      pieStrokeColor: '#000000', pieOuterStrokeColor: '#808080',
    };
    const mermaidLightVars = {
      background:          '#d4d0c8',
      mainBkg:             '#d4d0c8',
      primaryColor:        '#d4d0c8',
      primaryTextColor:    '#000000',
      primaryBorderColor:  '#660099',
      lineColor:           '#404040',
      textColor:           '#000000',
      secondaryColor:      '#b0b0b0',
      clusterBkg:          '#d4d0c8',
      clusterBorder:       '#606060',
      nodeBorder:          '#660099',
      edgeLabelBackground: '#d4d0c8',
      noteBkgColor:        '#d4d0c8',
      noteTextColor:       '#000000',
      noteBorderColor:     '#606060',
      archEdgeColor:       '#404040',
      archGroupBorderColor: '#606060',
      pie1: '#0019ee', pie2: '#8b005c', pie3: '#005500', pie4: '#5a4a00',
      pieSectionTextColor: '#c0c0c0',
      pieStrokeColor: '#c0c0c0', pieOuterStrokeColor: '#404040',
    };
    mermaid.initialize({
      startOnLoad: true, theme: 'base', look: 'classic',
      securityLevel: window.mermaidSecurityLevel || 'strict',
      pie: { textPosition: 0.65 },
      fontFamily: mermaidFont,
      themeVariables: {
        darkMode: !mermaidLight,
        fontFamily: mermaidFont,
        fontSize:   '1rem',
        pieOpacity: '1',
        pieTitleTextSize: '1.15rem', pieStrokeWidth: '1.5px', pieOuterStrokeWidth: '1px',
        ...(mermaidLight ? mermaidLightVars : mermaidDark),
      },
    });
    const overlay = document.getElementById('mermaid-zoom');
    if (!overlay) throw new Error('mermaid.js requires <dialog class="mermaid-overlay" id="mermaid-zoom"></dialog> as the first child of <body>');
    const zoomLabel = window.mermaidZoomLabel || 'Zoom diagram';
    const regionLabel = window.mermaidRegionLabel || 'Scrollable diagram';
    const titleOf = svg => svg.querySelector('title')?.textContent?.trim();
    const named = (svg, label) => {
      const title = titleOf(svg);
      return title ? label + ': ' + title : label;
    };
    const hide = () => {
      overlay.classList.remove('active');
      overlay.close();
      overlay.innerHTML = '';
    };
    const zoom = svg => {
      const zoomed = svg.cloneNode(true);
      zoomed.removeAttribute('width');
      zoomed.removeAttribute('height');
      zoomed.style.maxWidth = zoomed.style.width = zoomed.style.height = '';
      overlay.setAttribute('aria-label', named(svg, zoomLabel));
      overlay.replaceChildren(zoomed);
      overlay.showModal();
      requestAnimationFrame(() => overlay.classList.add('active'));
    };
    const scrolls = window.matchMedia('(max-width: 600px)');
    const syncRegions = () => {
      document.querySelectorAll('pre.mermaid').forEach(pre => {
        const svg = pre.querySelector('svg');
        if (!svg) return;
        if (scrolls.matches) {
          pre.tabIndex = 0;
          pre.setAttribute('role', 'region');
          pre.setAttribute('aria-label', regionLabel);
        } else {
          pre.removeAttribute('tabindex');
          pre.removeAttribute('role');
          pre.removeAttribute('aria-label');
        }
      });
    };
    scrolls.addEventListener('change', syncRegions);
    const zoomBound = new WeakSet();
    document.querySelectorAll('pre.mermaid').forEach(pre => {
      new MutationObserver(() => {
        const svg = pre.querySelector('svg');
        if (!svg) return;
        if (!zoomBound.has(svg)) {
          zoomBound.add(svg);
          svg.addEventListener('click', e => { if (!e.target.closest('a')) zoom(svg); });
        }
        if (svg.style.maxWidth) svg.style.setProperty('--natural-width', svg.style.maxWidth);
        syncRegions();
        if (!pre.querySelector('.mermaid-zoom')) {
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'mermaid-zoom';
          button.textContent = zoomLabel;
          button.setAttribute('aria-label', named(svg, zoomLabel));
          button.addEventListener('click', () => zoom(svg));
          pre.append(button);
        }
      }).observe(pre, { childList: true });
    });
    overlay.addEventListener('click', hide);
    overlay.addEventListener('cancel', e => { e.preventDefault(); hide(); });
  </script>
