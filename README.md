# Proximity-indices-between-technologies-applied-to-OpenAlex

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation and use</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This projects aims at measuring the proximity between cybersecurity technologies under the form of time series based on bibliometric data taken from Openalex.

The project is divided in 3 parts: the creation of the data, the exploration of the data, and the creation, visualization and forecasting of proximity indices. Each part is contained in one specific folder. Each folder contains a file called "directory_file" + something specific to the specific folder. If you run this file, it runs all the other files contained in this folder in the right order.
At the same level of the folders, there is a file called "directory_file", which runs all the directory files specific to each folder in the right order.
Once this is done, one can simply run the main directory file and then all the files are ran. Note that the whole computations might take approximately a week to be run.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.


* Darts [-->][darts]
* Sktime [-->][sktime]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Give a list of all the libraries required to run my work.
* keybert~=0.6.0 
  ```sh
  pip install keybert
  ```
* tqdm~=4.64.1
  ```sh
  conda install -c conda-forge tqdm
  ```
* nltk~=3.7
  ```sh
  conda install -c anaconda nltk
  ```
* pandas~=1.4.4
  ```sh
  conda install -c anaconda pandas
  ```  
* numpy~=1.22.4
  ```sh
  conda install -c anaconda numpy
  ```
* sktime~=0.14.1
  ```sh
  conda install -c conda-forge sktime
  ```
* yellowbrick~=1.5
  ```sh
  conda install yellowbrick=1.5
  ```
* torch~=1.13.1
  ```sh
  conda install -c pytorch pytorch
  ```
* tslearn~=0.5.2
  ```sh
  conda install tslearn=0.5.2
  ```
* darts~=0.21.0
  ```sh
  conda install -c conda-forge darts
  ```
* scikit-learn~=1.0.2
  ```sh
  conda install scikit-learn=1.0.2
  ```
* scipy~=1.9.3
  ```sh
  conda install scipy=1.9.3
  ```
* seaborn~=0.12.0
  ```sh
  conda install seaborn=0.12.0
  ```
* optuna~=2.10.1
  ```sh
  conda install optuna=2.10.1
  ```
* matplotlib~=3.5.3
  ```sh
  conda install matplotlib=3.5.3
  ```
* requests~=2.28.1
  ```sh
  conda install requests=2.28.1
  ```
  

  ( )
 ()




### Installation and use

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Download all the folders somewhere in your laptop
2. Download manually "m4_monthly_scaled.pkl" and "m4_monthly_scaled.pkl" from https://github.com/unit8co/amld2022-forecasting-and-metalearning/tree/main/data and to put them in the folder called "indices_proximity". These files are used then for the transfer learning part and I could not download them automatically, because of some technical problems.
3. Run "directory_file"


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->


[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png


[sktime]: https://www.sktime.org/en/stable/
[darts]: https://unit8co.github.io/darts/

