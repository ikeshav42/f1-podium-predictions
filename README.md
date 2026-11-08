# F1 podium predictions

Before each race this season I predict the podium from the qualifying result and write about it on LinkedIn and Medium. This repo has one notebook per race, so you can see exactly how each prediction was made and check it against what happened.

All notebooks are the same template. Only the settings cell at the top changes (session numbers, circuit, penalties).

## Scorecard

| Race | Predicted podium | Actual podium | Right |
|---|---|---|---|
| Mexico City (1 Nov) | Russell, Verstappen, Hamilton | Verstappen, Hamilton, Antonelli | 2 of 3 |
| Brazil (8 Nov), first version | Russell, Norris, Verstappen | Norris, Verstappen, Hadjar | 2 of 3 |
| Brazil (8 Nov), corrected version | Russell, Norris, Leclerc | Norris, Verstappen, Hadjar | 1 of 3 |

Notes on the table:

- Mexico was re-run after the race with the final version of the code, using only data from before the race. The picks can differ from what I posted at the time.
- Brazil: the first version was committed on 7 Nov, before the race, but it used the raw qualifying order, which was wrong because it ignored the penalties (it had Verstappen 16th, he started 21st, and Russell, Leclerc, Hamilton and others had penalties too). I corrected the grid and re-ran it during the race, committed 8 Nov 17:43 UTC, so the corrected picks (Russell, Norris, Leclerc) are not a true pre-race prediction. The first version had Russell, Norris and Verstappen.
- The official grid had Verstappen 21st and Perez 22nd. I put Verstappen 22nd in the corrected run, so that was one slot off.
- Hadjar (5th on the real grid) was the surprise podium, the model gave him about 10%.
- The Mexico notebook was re-run with the same grid handling as Brazil. The picks did not change.
- I will keep the misses in the table.

## How it works

1. Download race results (Jolpica / Ergast, through fastf1) and weather and practice times (OpenF1).
2. Build inputs for every driver in every past race: starting position, average finish and points over the last 5 races, podium rate, the team's recent points, and the driver's recent finishes at the same circuit.
3. Test 7 scikit-learn models walking forward through every race since the start of 2025. For each race the model is trained on earlier races only, then predicts that race's podium. The score is how many of the 3 picked drivers really finished on the podium.
4. Keep the best model and use it on the new grid.

Models tested: logistic regression, decision tree, random forest, extra trees, gradient boosting, histogram gradient boosting and XGBoost. The comparison to beat is "the top 3 on the grid are the podium".

## What I found

For Brazil, over 43 races the best model gets 2.19 of 3 podium drivers right per race, and the grid rule gets 2.07. That is a small edge and I would not call it proven. The models mostly agree with the grid and then move a few drivers up or down based on recent form.

Things that did not help:

- practice pace (best lap gap to the fastest car in practice)
- how wet qualifying was
- recent form without the grid (clearly worse)

Only a handful of past qualifying sessions were wet, so the rain input does not have much to learn from.

## Limitations

- Penalties are added by hand in the settings cell, from news and race control messages. Check them.
- The weather forecast for race day is not an input.
- The test set is about 43 races, so small differences between models are mostly luck.
- A driver who starts far back with strong recent form (Verstappen in Brazil) is where the models disagree most. In the 2023 to 2026 data, 5 of 23 such drivers reached the podium.

## Running it

```
pip install -r requirements.txt
```

Open a notebook in `notebooks/` and run all cells. The first run takes a few minutes because it downloads about 90 race weekends from OpenF1, after that it reads from a local cache folder. OpenF1 blocks access while a session is running, so run it between sessions.

`make_card.py` draws the podium image from a predictions csv, for example:

```
python make_card.py predictions/brazil_2026.csv "Brazilian GP 2026" "Predicted podium after a wet qualifying" images/brazil_podium_card.png
```

## Data and credit

- Results: Jolpica (Ergast API) through [fastf1](https://github.com/theOehrly/Fast-F1)
- Weather and practice times: [OpenF1](https://openf1.org)
- Thanks to [Mariana Antaya](https://github.com/mar-antaya) for her F1 prediction project, which got me started on this.

This is a personal project and it is not affiliated with Formula 1.

## License

MIT, see [LICENSE](LICENSE).
