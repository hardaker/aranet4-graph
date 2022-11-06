# Graph data file(s) from an aranet4 sensor

aranet4-graph takes a YAML file as input.

Example:

``` yaml
file: 2022-11-05-smf-to-lhr.csv
begin: "2022-11-04 08:23 PDT"
markers:
       "2022-11-04 09:00 PDT": "at home"
       "2022-11-04 11:30 PDT": "SMF gate"
       "2022-11-04 12:20 PDT": "boarding"
       "2022-11-04 13:05 PDT": "taking off"
       "2022-11-04 13:55 PDT": "in flight"
       "2022-11-04 16:14 MDT": "landing"
       "2022-11-04 16:45 MDT": "DEN United club"
       "2022-11-04 17:45 MDT": "at next gate"
end:   "2022-11-04 18:45 MDT"
```

# Installation

    pipx install aranet4-graph

or
    pip install aranet4-graph

# Example output

![Example output image](images/example.png)

# Source code

https://github.com/hardaker/aranet4-graph
