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

This projects aims at creating and measuring the evolution of the proximity between cybersecurity technologies under the form of time series based on bibliometric (text mining) data taken from Openalex.

The project is divided in 3 parts: (i) the collection of raw data, (ii) the exploration and transformation (EDA) of the data, and (iii) the creation, visualization and forecasting of proximity indices (extracted from raw data). Each part is contained in one specific folder. Each folder contains a file called "directory_file". If you run this file, it runs all the other files contained in the folder (in the right order).
Nevertheless, some libraries must be installed before running the main directory file. This can be found in "getting started".

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Darts [-->][darts]
* Sktime [-->][sktime]
* Scipy [-->][scipy]
* Keybert [-->][keybert]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Structure of the repository

The repository contains several folders each dedicated to specific task of the project.

* creation_data_and_variables
 This folder contains all the files which create the different pandas dataframes of variables.
* exploratory_analysis
 This folder contains all the files which explore and visualize the data generated in the previous folder.
* indices_proximity
 This folder contains all the files which generate, explore, visualize, process, cluster and forecast time series of 
 indices of technological proximity.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

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
  

### Installation and use

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Download all the folders in your laptop
2. Download manually "m4_monthly_scaled.pkl" and "m4_monthly_scaled.pkl" from https://github.com/unit8co/amld2022-forecasting-and-metalearning/tree/main/data and to put them in the folder called "indices_proximity". These files are used then for the transfer learning part and I could not download them automatically, because of some technical problems.
3. Download all the libraries mentionned above.
4. Once this is done, one can simply run the main directory file and then all the files are ran. Note that the whole computations might take approximately a week to be run.


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


<!-- CONTACT -->
## Contact

Alessandro Tavazzi - tavazale@gmail.com

Project Link: [https://github.com/technometrics-lab/Proximity-indices-applied-to-OpenAlex](https://github.com/technometrics-lab/Proximity-indices-applied-to-OpenAlex)

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
[scipy]: https://scipy.org/
[keybert]: https://pypi.org/project/keybert/
