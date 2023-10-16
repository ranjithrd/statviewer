from src.aggregate.utils.percentile import percentile
import src.aggregate.utils.percentile as percentile
from src.data.load import allData

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
    splitFunction = lambda m : percentile.percentile(valueFunction, m, allMatches)
    return splitAcrossSeasons(splitFunction, matches)

def generateDataPoints(dataFunction, matches, key, ad):
    return {
        "%s"%(key,): dataFunction(matches),
        "%s_percentile"%(key,): percentile.percentile(lambda m: dataFunction(m), matches, ad),
        "%s_split_seasons"%(key,): splitAcrossSeasons(dataFunction, matches),
        "%s_percentile_split_seasons"%(key,): splitPercentileAcrossSeasons(dataFunction, matches, ad)
    }