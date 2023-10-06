def calculatePercentile(value, data):
    sortedData = sorted(data)

    if value not in sortedData:
        # simulate index
        data.append(value)
        sortedData = sorted(data)

    return round(100 * ((sortedData.index(value) + 1) / len(data)))

# VALUE_FUNCTION MUST TAKE THE RECORD AND
# *NOT AN INDIVIDUAL ATTRIBUTE*


def percentile(valueFunction, forRecord, inData):
    dataRange = []
    for i in inData:
        dataRange.append(valueFunction(i))

    return calculatePercentile(valueFunction(forRecord), dataRange)
