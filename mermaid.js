  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@12.0.0/dist/mermaid.esm.min.mjs';
    const mermaidLight = getComputedStyle(document.documentElement).getPropertyValue('--mermaid-scheme').trim() === 'light';
    const mermaidFont = '"JetBrains Mono", ui-monospace, "Fira Code", monospace';
    const mermaidDark = {
      background:          '#44475a',
      mainBkg:             '#44475a',
      primaryColor:        '#44475a',
      primaryTextColor:    '#f8f8f2',
      primaryBorderColor:  '#bd93f9',
      lineColor:           '#6272a4',
      textColor:           '#f8f8f2',
      secondaryColor:      '#1e1f29',
      clusterBkg:          '#44475a',
      clusterBorder:       '#707388',
      nodeBorder:          '#bd93f9',
      edgeLabelBackground: '#44475a',
      noteBkgColor:        '#44475a',
      noteTextColor:       '#f8f8f2',
      noteBorderColor:     '#707388',
      archEdgeColor:       '#6272a4',
      archGroupBorderColor: '#707388',
      pie1: '#8be9fd', pie2: '#ff79c6', pie3: '#50fa7b', pie4: '#f1fa8c',
      pieSectionTextColor: '#282a36',
      pieStrokeColor: '#282a36', pieOuterStrokeColor: '#6272a4',
    };
    const mermaidLightVars = {
      background:          '#cfcfde',
      mainBkg:             '#cfcfde',
      primaryColor:        '#cfcfde',
      primaryTextColor:    '#1f1f1f',
      primaryBorderColor:  '#644ac9',
      lineColor:           '#6c664b',
      textColor:           '#1f1f1f',
      secondaryColor:      '#cfcfde',
      clusterBkg:          '#cfcfde',
      clusterBorder:       '#7b7f94',
      nodeBorder:          '#644ac9',
      edgeLabelBackground: '#cfcfde',
      noteBkgColor:        '#cfcfde',
      noteTextColor:       '#1f1f1f',
      noteBorderColor:     '#7b7f94',
      archEdgeColor:       '#6c664b',
      archGroupBorderColor: '#7b7f94',
      pie1: '#036a96', pie2: '#a3144d', pie3: '#14710a', pie4: '#846e15',
      pieSectionTextColor: '#fffbeb',
      pieStrokeColor: '#fffbeb', pieOuterStrokeColor: '#6c664b',
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
