<br/>
<p align="center">
  <a href="https://github.com/rhijjawi/ManageBac-API">
    <img src="https://s3.imgcdn.dev/UcujO.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">ManageBac Scraper</h3>

  <p align="center">
    ManageBac Scraper that uses session cookies valid for 1 year.
    <br/>
    <br/>
    <a href="https://github.com/rhijjawi/ManageBac-API">View Demo</a>
    .
    <a href="https://github.com/rhijjawi/ManageBac-API/issues">Report Bug</a>
    .
    <a href="https://github.com/rhijjawi/ManageBac-API/issues">Request Feature</a>
  </p>
</p>

![License](https://img.shields.io/github/license/rhijjawi/ManageBac-API) 

## About The Project

![Screen Shot](images/screenshot.png)

ManageBac has been lacking in terms of APIs accessible by students. I set off to make a web-scraper for students that allows them to turn their ManageBac portal into `json` parse-able content.

## Built With

`Python 3.8`
`BeautifulSoup4`
`Requests`

`Node.js`
`cheerio`
`jssoup`

## Getting Started

`pip install managebac_api`

### Prerequisites

It's used as a function, pretty easy stuff

### Installation

pip install managebac_api
```py
import managebac_api
from managebac_api import managebac_api


managebac_api.mbapi(domain, cookie)
```

## Usage

```py
managebac_api.mbapi("IBS","o1h98dh93hr2r32d...")
```
1st part of the function is the subdomain that you use for managebac. In this case IBS.managebac.com would be what the student normally visits
2nd part is the session cook that you can get can get by look in the dev console (F12)

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/rhijjawi/ManageBac-API/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/rhijjawi/ManageBac-API/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/rhijjawi/ManageBac-API/blob/main/LICENSE.md) for more information.

## Authors

* **Ramzi Hijjawi** - *Python Programmer* - [Ramzi Hijjawi](https://github.com/rhijjawi/) - *Designed from the ground up*

## Acknowledgements

* [Ramzi Hijjawi](https://github.com/rhijjawi/)

