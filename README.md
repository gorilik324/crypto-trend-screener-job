# crypto-trend-screener-job
Application for searching the intraday, swing trends on the USDT perpetual futures markets of the Bybit exchange.

# About
Batch job looking for trends across the USDT perpetual futures market on the Bybit exchange.
The application recognizes intraday trends based on the D chart, swing trends based on the W and M charts.
The output of the program is an excel file.

## Development
Application is actively maintenance and develop.

## Installation
```commandline
make clean
make prepare
```

## Usage
**Run job**
```commandline
make run
libreoffice CryptoTrendScreener_YYYYMMDD.xlsx
```

**Find trade opportunities (example intraday)**
* Long
  * Open the sheet "Intraday D trends"
  * Sort by the market that grew the most by colum "Change 7 days, %"
  * Filter markets by context (Up-trend, Start rotation after up-trend) 

* Short
  * Open the sheet "Intraday D trends"
  * Sort by the market that decline the most by colum "Change 7 days, %"
  * Filter markets by context (Up-trend, Start rotation after up-trend) 


## Contact
You can reach out for support on the [GeorgeQuantAnalyst](https://t.me/GeorgeQunatAnalyst) telegram chat.

## Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
     <td align="center"><a href="https://github.com/GeorgeQuantAnalyst"><img src="https://avatars.githubusercontent.com/u/112611533?v=4" width="100px;" alt=""/><br /><sub><b>GeorgeQuantAnalyst</b></sub></a><br /><a href="https://github.com/GeorgeQuantAnalyst" title="Ideas">🤔</a></td>
    <td align="center"><a href="https://github.com/LucyQuantAnalyst"><img src="https://avatars.githubusercontent.com/u/115091833?v=4" width="100px;" alt=""/><br /><sub><b>LucyQuantAnalyst</b></sub></a><br /><a href="https://github.com/LucyQuantAnalyst" title="Code">💻</a></td>
  </tr>
</table>
