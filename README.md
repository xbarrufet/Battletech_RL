<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
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

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

-->



<!-- PROJECT LOGO
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>
-->


<!-- TABLE OF CONTENTS
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


The ultimate goal of this repo is to implement a trained system to play Battletech. I'm not a reinforcemnet learning expert and this is developed to learn about it, not to create a professional system

I'm developing it in different phases based on the Battltech rules flavours, starting with the beginning box 1-on-1 system and moving forward ( I hope)


<!-- ROADMAP -->
## Roadmap

- [x] Beginning Rules V1
  - [x] 1-on-1 movement 
  - [ ] 1-on-1 Firing
- [ ] Multi-Mech support
- [ ] ..will see
    

## Beginning Rules V1

### Obsevation Space
Current Observation Space contains
* Mech positions and Facing
* Mech distances
* Movement Type done
* Visibilty (is in frontal Arc?)

### Action Space
Movement action space contains all possible movements, this is:
* Number of Board Cells (15x17) x Facing (6) x Movement Type (3 walk, run, jump)
The simulation environment returns all allowed movements based as a bits array included within the observations3

### Considerations
Current development is on the implementation of 1-on-1 system under certain premises
* Simulation uses impacts probabilities as damage% to avoid stochastic processes
* Trasverssed Hex is reduced to distance
* Firing system is Automatic and all weapons are fired in a row
* First Version is based on Policy Gradient algorithm

### Change log
28/08/24: Initial Version
* Environment
* Basic Modelling
* Policy Gradient Agent for Movement calculation
  * Rewards based on probabilty the obtain a hit calcultaing all the dice modifiers (GATOR) 






