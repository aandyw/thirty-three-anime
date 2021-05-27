<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
<!--   <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h1 align="center">The Anime 3x3</h1>

  <p align="center">
    An anime recommender system that hits different.
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#technologies-used">Technologies used</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#project-structure">Project Structure</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [App demo](https://example.com) -->
A web-based recommender system that infers the user's anime preference based on their 9 selected anime.

### Technologies used

* HTML/CSS/JS
* [Bootstrap](https://getbootstrap.com/)
* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [Sklearn](https://scikit-learn.org/stable/)
* [Jikan API](https://jikan.moe/)


<!-- GETTING STARTED -->
## Getting Started

### Project Structure
* [`/`](/../../): where you're reading this...hopefully
* [`data/`](data/): a partial dataset of the [myanimelist kaggle dataset](https://www.kaggle.com/azathoth42/myanimelist)
* [`recsys/`](recsys/): experimental recommender algorithms that we're looking into
* [`utils/`](utils/): scripts for data-preparation/processing

To get a local copy up and running follow these simple steps.

### Prerequisites

A list of pip packages are listed in `requirements.txt`. To set up your environment run the following command
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Create a django project
   ```sh
   django-admin startproject anime33
   ```
2. Clone the repo
   ```sh
   git clone https://github.com/Pie31415/thirty-three-anime.git
   ```
   and move the contents of [`anime33`](anime33/) to your newly created django project
3. Run the app
   ```sh
   cd anime33
   python manage.py runserver
   ```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [This awesome README](https://github.com/othneildrew/Best-README-Template)
* [Anime Jikan Search Tutorial](https://www.youtube.com/watch?v=AI5lsNeVyO8)
* [Prototyping A RecSys](https://towardsdatascience.com/prototyping-a-recommender-system-step-by-step-part-1-knn-item-based-collaborative-filtering-637969614ea)
* [Very nice loaders](https://loading.io/css/)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Pie31415/thirty-three-anime.svg?style=for-the-badge
[contributors-url]: https://github.com/Pie31415/thirty-three-anime/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Pie31415/thirty-three-anime.svg?style=for-the-badge
[forks-url]: https://github.com/Pie31415/thirty-three-anime/network/members
[stars-shield]: https://img.shields.io/github/stars/Pie31415/thirty-three-anime.svg?style=for-the-badge
[stars-url]: https://github.com/Pie31415/thirty-three-anime/stargazers
[license-shield]: https://img.shields.io/github/license/Pie31415/thirty-three-anime.svg?style=for-the-badge
[license-url]: https://github.com/Pie31415/thirty-three-anime/blob/master/LICENSE.txt
