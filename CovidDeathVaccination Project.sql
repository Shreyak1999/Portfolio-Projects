---Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types

SELECT location, date, total_cases, new_cases, total_deaths, population FROM CovidDeaths$
WHERE continent IS NOT NULL
ORDER BY 1,2

--Total Cases VS Total Deaths
---- This displays the death rate among infected due to contacting the Novelcorona Virus between early 2020 and mid 2021.
SELECT location, date, total_cases, total_deaths, (total_deaths*100/total_cases) AS Death_Rate
FROM CovidDeaths$
WHERE location = 'India'
ORDER BY 1,2
---- The trends indicate a decrease in the death rate among infected over a 1.3-year period in India. 

--Peak Death Rate among Infected in India
SELECT ROUND(MAX(total_deaths*100/total_cases),3) AS Peak_Death_Rate
FROM CovidDeaths$ 
WHERE location = 'India'

SELECT date 
FROM CovidDeaths$
WHERE (total_deaths*100/total_cases) > 3.59587180879956 AND location = 'India'
---- The death incidence among infected in India peaked at 3.596% in April, 2020


--Total Cases VS Population
SELECT location, date, population, total_cases, (total_cases*100/population) AS Infection_Rate
FROM CovidDeaths$
WHERE location = 'India'
ORDER BY 1,2


-- Highest Infection Rates Across the World
SELECT location, population, Max(total_cases) AS High_Infec_Count
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY 3 DESC

SELECT location, population, Max(total_cases) AS High_Infec_Count, Max((total_cases*100/population))
AS Peak_Infection_Rate
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY 4 DESC
---- The analysis shows that while India ranked 2nd globally in total COVID-19 cases due to its large population,
---- its infection rate relative to its total population was significantly lower compared to developed 
---- countries like the United States, France, and Luxembourg.


-- Highest Death Counts Across the World
SELECT location, Max(Cast(total_deaths AS INT)) AS Death_Count
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY Death_Count DESC
---- The analysis shows that the highest number of deaths was in the US, Brazil, and Mexico, which have significantly
---- lower populations as compared to India.


-- Continent Analysis of Death Count per Total Cases
SELECT location AS Continent, population, Max((total_deaths/total_cases)*100) AS Death_Rate_Cont
FROM CovidDeaths$
WHERE continent IS NULL
GROUP BY location, population
ORDER BY Death_Rate_Cont DESC
---- While Asia boasts the highest population in the world, incidence of death due to the novelcorona virus was
---- highest in Europe, North America and South America during the time period.



-- Analysis at the Global Level
SELECT date, SUM(new_cases) AS Total_Cases, SUM(CAST(new_deaths AS INT)) AS Total_Deaths, 
ROUND(SUM(CAST(new_deaths AS INT))*100/SUM(new_cases),3) AS Death_Rate
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2


SELECT * FROM CovidDeaths$ cd
JOIN CovidVaccinations$ cv
	ON cd.location=cv.location
	AND cd.date=cv.date

-- Total Population vs Vaccinations
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations
, SUM(CAST(COALESCE(cv.new_vaccinations,0) AS BIGINT)) OVER (PARTITION BY cd.location ORDER BY cd.location,cd.date) 
AS Daily_Vaccination
FROM CovidDeaths$ cd
JOIN CovidVaccinations$ cv
	ON cd.location=cv.location
	AND cd.date=cv.date
WHERE cd.continent IS NOT NULL
ORDER BY 2,3

--USING CTE
WITH CTE (continent, location, date, population, new_vaccination, Daily_Vaccination) 
AS (
    SELECT cd.continent, cd.location, cd.date, cd.population, 
           cv.new_vaccinations,
           SUM(CAST(COALESCE(cv.new_vaccinations, 0) AS BIGINT)) 
           OVER (PARTITION BY cd.location ORDER BY cd.location, cd.date) AS Daily_Vaccination
    FROM CovidDeaths$ cd
    JOIN CovidVaccinations$ cv
        ON cd.location = cv.location
        AND cd.date = cv.date
    WHERE cd.continent IS NOT NULL
)
SELECT *, 
       (Daily_Vaccination * 100.0 / population) AS Vaccination_Rate 
FROM CTE;

--USING Temp Tables
DROP TABLE IF EXISTS #Percent_People_Vaccinated
CREATE TABLE #Percent_People_Vaccinated
(continent NVARCHAR(255),
location NVARCHAR(255),
date DATETIME,
population NUMERIC,
new_vaccination NUMERIC,
Daily_Vaccination NUMERIC)
INSERT INTO #Percent_People_Vaccinated
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations
, SUM(CAST(COALESCE(cv.new_vaccinations,0) AS BIGINT)) OVER (PARTITION BY cd.location ORDER BY cd.location,cd.date) 
AS Daily_Vaccination
FROM CovidDeaths$ cd
JOIN CovidVaccinations$ cv
	ON cd.location=cv.location
	AND cd.date=cv.date
WHERE cd.continent IS NOT NULL
ORDER BY 2,3

SELECT * FROM #Percent_People_Vaccinated
ORDER BY 2,3




-- CREATING VIEWS FOR LATER PURPOSES
CREATE VIEW Vaccination_Rate AS
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations
, SUM(CAST(COALESCE(cv.new_vaccinations,0) AS BIGINT)) OVER (PARTITION BY cd.location ORDER BY cd.location,cd.date) 
AS Daily_Vaccination
FROM CovidDeaths$ cd
JOIN CovidVaccinations$ cv
	ON cd.location=cv.location
	AND cd.date=cv.date
WHERE cd.continent IS NOT NULL


CREATE VIEW High_Infec_Count AS
SELECT location, population, Max(total_cases) AS High_Infec_Count
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY location, population


CREATE VIEW Peak_Infection_Rate AS
SELECT location, population, Max(total_cases) AS High_Infec_Count, Max((total_cases*100/population))
AS Peak_Infection_Rate
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY location, population

CREATE VIEW Peak_Death_Count AS
SELECT location, Max(Cast(total_deaths AS INT)) AS Death_Count
FROM CovidDeaths$
WHERE continent IS NOT NULL
GROUP BY location

CREATE VIEW Continental_Death_Rate AS
SELECT location AS Continent, population, Max((total_deaths/total_cases)*100) AS Death_Rate_Cont
FROM CovidDeaths$
WHERE continent IS NULL
GROUP BY location, population


