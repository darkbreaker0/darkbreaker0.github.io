---
title: "CV"
layout: gridlay
sitemap: false
permalink: /cv/
---

## Curriculum Vitae

<p><a class="btn-pill btn-pdf" href="{{ site.url }}{{ site.baseurl }}/{{ site.links.cv }}" target="_blank">Download full CV (PDF)</a></p>

<div class="section-card">
<div class="pi-card">
<img src="{{ site.url }}{{ site.baseurl }}/images/{{ site.photo }}" class="pi-photo" alt="{{ site.name }}" loading="lazy">
<div>
<h3 class="pi-name">{{ site.name }}</h3>
<p style="font-style: italic; color: var(--text-secondary);">{{ site.title }}, {{ site.institution }}</p>
<div class="pi-links">
{% if site.email %}<a href="mailto:{{ site.email }}" class="icon-link" title="Email"><i class="fa-solid fa-envelope"></i></a>{% endif %}
{% if site.links.cv and site.links.cv != "" %}<a href="{{ site.url }}{{ site.baseurl }}/{{ site.links.cv }}" class="icon-link" title="CV"><i class="ai ai-cv"></i></a>{% endif %}
{% if site.links.google_scholar and site.links.google_scholar != "" %}<a href="{{ site.links.google_scholar }}" class="icon-link" title="Google Scholar"><i class="ai ai-google-scholar"></i></a>{% endif %}
{% if site.links.github and site.links.github != "" %}<a href="{{ site.links.github }}" class="icon-link" title="GitHub"><i class="fa-brands fa-github"></i></a>{% endif %}
{% if site.links.researchgate and site.links.researchgate != "" %}<a href="{{ site.links.researchgate }}" class="icon-link" title="ResearchGate"><i class="ai ai-researchgate"></i></a>{% endif %}
{% if site.links.orcid and site.links.orcid != "" %}<a href="{{ site.links.orcid }}" class="icon-link" title="ORCID"><i class="ai ai-orcid"></i></a>{% endif %}
{% if site.links.linkedin and site.links.linkedin != "" %}<a href="{{ site.links.linkedin }}" class="icon-link" title="LinkedIn"><i class="fa-brands fa-linkedin"></i></a>{% endif %}
</div>
{% if site.data.pi[0].education %}
<ul style="margin-top: var(--space-4);">
{% for education in site.data.pi[0].education %}
<li>{{ education | replace: "-","&#8211;" }}</li>
{% endfor %}
</ul>
{% endif %}
</div>
</div>
</div>

<div class="section-card" markdown="1">
### Research experience
- **2017–present — Postdoctoral Researcher**, DZNE, Bonn (Bradke Lab). Mechanics of CNS neuronal polarization; the Arp2/3–actomyosin local-excitation/global-inhibition system; quantitative neurite-growth analysis (R / ImageJ).
- **2014–2017 — Postdoctoral Researcher**, ZMBH, University of Heidelberg (Schiebel Lab). MOZART1 and the γ-tubulin small complex in *Candida albicans* and human cells.
- **2009–2014 — Doctoral Researcher**, ZMBH, University of Heidelberg (Schiebel Lab). Phospho-regulation of γ-TuSC and its receptors; targeting of γ-tubulin complexes to microtubule organizing centers.
</div>

{% if site.data.awards %}
<div class="section-card">
<h3>Honors &amp; fellowships</h3>
<ul>
{% for award in site.data.awards %}
<li>{{ award.name | replace: "-","&#8211;" }}</li>
{% endfor %}
</ul>
</div>
{% endif %}

<div class="section-card" markdown="1">
### Invited talks (selected)
- Microtubules in Neurons, Chiemsee (2023)
- The Cytoskeleton of Neurons and Glia, webinar series (2023)
- EMBO Workshop *Neural Development and Neurodegeneration*, Taipei (2022)
- FENS Symposium, Paris (2022)
- CSHL meeting *Molecular Mechanisms of Neuronal Connectivity*, New York (2022)
- European Cytoskeleton Forum, Hannover (2022)
- Invited lecture (with F. Bradke), NYCU College of Life Sciences, Taiwan (2022) — [watch ▶](https://www.youtube.com/watch?v=Kd7ejCS3kHg)
</div>

{% if site.data.people %}
<div class="section-card">
<h3>Student supervision</h3>
<ul>
{% for student in site.data.people %}
<li>{{ student.name }}, {{ student.location }} ({{ student.degree }}, {{ student.year }})</li>
{% endfor %}
</ul>
</div>
{% endif %}

<div class="section-card" markdown="1">
### Teaching & service
- Coordinator & lecturer, M.Sc. "Molecular Cell Biology" module, University of Bonn (2020–2023): light-microscopy basics, live-cell imaging, and data visualization with R.
- Associate Faculty Member, F1000 / Faculty Opinions (2019–present).
- Professional development: EMBO Laboratory Leadership and Project Management for Group Leaders; advanced courses at CSHL and EMBL.
</div>
