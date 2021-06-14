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

  <h1 align="center">The Anime 3x3</h1>

  <p align="center">
    An anime recommender system that hits different
    <br />
    <a href="https://fierce-thicket-59912.herokuapp.com/">View The Website</a>
  </p>
</p>

![App demo](https://github.com/Pie31415/thirty-three-anime/blob/main/demo/anime33demo.gif)


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
The Anime 3x3 is a web-based recommender system that we've developed to give people recommendations based on their submitted 3x3. Since the 3x3 is a collage of anime that describes your unique taste, our program looks at your 9 selected anime and trys to offer you similar shows based on your preference.

The algorithms that we have experimented with for the project include: K-Nearest Neighbors (KNN) and Matrix Factorization with Alternating Least Squares (ALS). However, the current system only uses the Sklearn KNN implementation as we've had the most success with it at the moment. The accuracy and efficieny of our current algorithm leaves much to be desired but it is a system that offers good enough results 50% of the time? Future features may include a deep-learning based approach or a more thorough look at content-based and collaborative filtering methods.


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
* [`data/`](data/): a partial/modified dataset of the [myanimelist kaggle dataset](https://www.kaggle.com/azathoth42/myanimelist)
* [`recsys/`](recsys/): experimental recommender algorithms that we are/have looked into
* [`utils/`](utils/): scripts for data-preparation/preprocessing of csv

To get a local copy up and running follow these simple steps.

### Prerequisites

A list of pip packages are listed in `requirements.txt`. To set up your environment run the following command
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/Pie31415/thirty-three-anime.git
   ```
   and move the contents of [`anime33/`](anime33/) to your newly created django project
   
2. Create an `.env` file with a `SECRET_KEY`

4. Run the app

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
* [Prototyping A RecSys](https://github.com/KevinLiao159/MyDataSciencePortfolio/tree/master/movie_recommender)
* [Large-Scale Parallel Collaborative Filtering for the Netflix Prize](https://www.researchgate.net/publication/220788980_Large-Scale_Parallel_Collaborative_Filtering_for_the_Netflix_Prize)
* [Recommending anime with KNN](https://gist.github.com/Tahsin-Mayeesha/81dcdafc61b774768b64ba5201e31e0a#file-recommending-anime-with-k-nearest-neighbor-ipynb)
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
