from aggregate.utils.percentile import percentile

# TAKES MATCHES AND A VALUE FUNCTION THAT RETURNS ANY VALUE FOR SEASON


def splitAcrossSeasons(valueFunction, matches):
    seasons = {}
    for i in matches:
        if i["year"] not in seasons:
            seasons[i["year"]] = []

        seasons[i["year"]].append(i)

    final = {}
    for k, v in seasons.items():
        final[k] = valueFunction(v)

    return final

# TAKES MATCHES AND A VALUE FUNCTION THAT
# RETURNS PERCENTILE OF ANY VALUE FOR SEASON


def splitPercentileAcrossSeasons(valueFunction, matches, allMatches):
    splitFunction = lambda m : percentile(valueFunction, m, allMatches)
    return splitAcrossSeasons(splitFunction, matches)