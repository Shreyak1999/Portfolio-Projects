-- Data Cleaning Project SQL
-- Skills Used: CAST, PARTITION BY, ALTER, UPDATE, JOINS, ROW NUMBER, SUBSTRING, PARSENAME, CASE, DROP

SELECT * FROM Housing

-- Standardize Date Formats

SELECT CAST(SaleDate AS Date) FROM Housing

ALTER Table Housing
ADD SaleDateConv Date
UPDATE Housing
SET SaleDateConv = CAST(SaleDate AS Date)

SELECT SaleDateConv FROM Housing


-- Fill Property Address
SELECT * FROM Housing
ORDER BY ParcelID

SELECT A.ParcelID, A.PropertyAddress, B.ParcelID, B.PropertyAddress, ISNULL(A.PropertyAddress, B.PropertyAddress)
FROM Housing A
JOIN Housing B
	ON A.ParcelID = B.ParcelID
	AND A.[UniqueID ] <> B.[UniqueID ]
WHERE A.PropertyAddress IS NULL

UPDATE A
SET PropertyAddress = ISNULL(A.PropertyAddress, B.PropertyAddress)
FROM Housing A
JOIN Housing B
	ON A.ParcelID = B.ParcelID
	AND A.[UniqueID ] <> B.[UniqueID ]
WHERE A.PropertyAddress IS NULL



-- Disaggregating the Property Address into Separate Columns (Address, City, State)
SELECT PropertyAddress FROM Housing

SELECT 
SUBSTRING(PropertyAddress,1,CHARINDEX(',',PropertyAddress)-1) AS Address,
SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress)+1, LEN(PropertyAddress)) AS City
FROM Housing

ALTER Table Housing
ADD PropSplitAdd NVARCHAR(255)
UPDATE Housing
SET PropSplitAdd = SUBSTRING(PropertyAddress,1,CHARINDEX(',',PropertyAddress)-1)

ALTER Table Housing
ADD PropSplitCity NVARCHAR(255)
UPDATE Housing
SET PropSplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress)+1, LEN(PropertyAddress))

SELECT PropSplitAdd, PropSplitCity FROM Housing

SELECT OwnerAddress
FROM Housing

-- Disaggregating the Owner Address into Separate Columns (Address, City, State)
SELECT OwnerAddress
FROM Housing

SELECT 
PARSENAME(REPLACE(OwnerAddress, ',', '.'),3) AS OwnerAdd,
PARSENAME(REPLACE(OwnerAddress, ',', '.'),2) AS OwnerCity,
PARSENAME(REPLACE(OwnerAddress, ',', '.'),1) AS OwnerState
FROM Housing

ALTER Table Housing
ADD OwnerSplitAdd NVARCHAR(255)
UPDATE Housing
SET OwnerSplitAdd = PARSENAME(REPLACE(OwnerAddress, ',', '.'),3)

ALTER Table Housing
ADD OwnerSplitCity NVARCHAR(255)
UPDATE Housing
SET OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress, ',', '.'),2)

ALTER Table Housing
ADD OwnerSplitState NVARCHAR(255)
UPDATE Housing
SET OwnerSplitState = PARSENAME(REPLACE(OwnerAddress, ',', '.'),1)

SELECT * FROM Housing


-- Change Y & N to Yes or No in Sold as Vacant as there are inconsistencies in them

SELECT DISTINCT SoldAsVacant FROM Housing

SELECT DISTINCT SoldAsVacant, COUNT(SoldAsVacant) FROM Housing
GROUP BY SoldAsVacant
ORDER BY 2

SELECT SoldAsVacant,
	CASE
		WHEN SoldAsVacant = 'Y' THEN 'Yes'
		WHEN SoldAsVacant = 'N' THEN 'No'
		Else SoldAsVacant
	END
FROM Housing

UPDATE Housing
SET SoldAsVacant = 
	CASE
		WHEN SoldAsVacant = 'Y' THEN 'Yes'
		WHEN SoldAsVacant = 'N' THEN 'No'
		ELSE SoldAsVacant
	END


-- Removing Duplicates
WITH CTE AS
(SELECT *,
ROW_NUMBER() OVER (
PARTITION BY ParcelID,
			PropertyAddress,
			SaleDate,
			LegalReference
			ORDER BY UniqueID) Row_num
FROM Housing
)
--DELETE FROM CTE
--WHERE Row_num>1

SELECT * FROM Housing




-- Remove Unused Columns
ALTER TABLE Housing
DROP COLUMN PropertyAddress, OwnerAddress, TaxDistrict

ALTER TABLE Housing
DROP COLUMN SaleDate
