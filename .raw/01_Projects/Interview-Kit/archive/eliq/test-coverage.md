# Test Coverage: Rules and Scenario Walkthrough

## Calculation Rules

Time bands (surface format `HHmm`):

- `0600-0629 => 9`
- `0630-0659 => 16`
- `0700-0759 => 22`
- `0800-0829 => 16`
- `0830-1459 => 9`
- `1500-1529 => 16`
- `1530-1659 => 22`
- `1700-1759 => 16`
- `1800-1829 => 9`
- outside ranges => `0`

Global rules:

- 60-minute rule: only highest charge in a 60-minute window is applied. Exactly 60 minutes apart starts a new window (strict `<`).
- Daily cap: max `60` per day.
- Toll-free days: weekends, July, configured toll-free dates.
- Average: `totalFee / allDistinctDays` (including toll-free days).
- Timezone basis: calculations use Gothenburg local time (UTC inputs are converted first).

---

## Unit and Service Scenarios

### `CongestionRuleEngineTests`

#### `GetFeeForPassage_ReturnsExpectedFee`

- Input data (Theory, all boundary timestamps on `2026-12-01`):
  - `06:00 => 9`, `06:29 => 9`
  - `06:30 => 16`, `06:59 => 16`
  - `07:00 => 22`, `07:15 => 22`, `07:59 => 22`
  - `08:00 => 16`, `08:29 => 16`
  - `08:30 => 9`, `14:59 => 9`
  - `15:00 => 16`, `15:29 => 16`
  - `15:30 => 22`, `16:59 => 22`
  - `17:00 => 16`, `17:59 => 16`
  - `18:00 => 9`, `18:29 => 9`
  - `05:59 => 0`, `18:30 => 0`, `00:00 => 0`, `23:59 => 0`
- Flow:
  - Convert each time to minute-of-day.
  - Match against fee-band ranges.
- Expected:
  - exact tariff lookup result per timestamp above.

#### `CalculateDailyFee_Within60Minutes_UsesHighestFee`

- Input data:
  - `07:00`, `07:40`, `08:20`
- Fee math:
  - `07:00(22)` and `07:40(22)` in first 60-minute window => `22`
  - `08:20(16)` starts new window (08:20 >= 08:00) => `+16`
  - total => `38`
- Expected: daily fee `38`.

#### `CalculateDailyFee_ExceedsCap_Returns60`

- Input data:
  - `06:00`, `07:10`, `08:20`, `09:40`, `15:00`, `16:10`
- Fee math:
  - windowed total `9 + 22 + 16 + 9 + 16 + 22 = 94`
  - daily cap applies.
- Expected: daily fee `60`.

#### `CalculateDailyFee_Exactly60MinutesApart_StartsNewWindow`

- Input data:
  - `07:00` and `08:00`
- Fee math:
  - `07:00(22)` window ends at `08:00`. `08:00` is NOT < `08:00` => new window.
  - `22 + 16 = 38`
- Expected: daily fee `38`.

#### `CalculateDailyFee_SinglePassage_ReturnsSingleFee`

- Input data: `07:10`
- Expected: `22`.

#### `CalculateDailyFee_PassageOutsideAllBands_ReturnsZero`

- Input data: `05:00` and `19:00`
- Expected: `0`.

#### `CalculateDailyFee_EmptyPassages_ReturnsZero`

- Input data: empty collection.
- Expected: `0`.

#### `CalculateDailyFee_EmptyFeeBands_ReturnsZero`

- Input data: passages with no fee bands configured.
- Expected: `0`.

#### `CalculateDailyFee_ThreeConsecutive60MinWindows_ChargesThreeSeparateFees`

- Input data:
  - `06:00`, `07:00`, `08:00`
- Fee math:
  - `06:00(9)` window ends `07:00`. `07:00` >= `07:00` => new window.
  - `07:00(22)` window ends `08:00`. `08:00` >= `08:00` => new window.
  - `08:00(16)`.
  - total `9 + 22 + 16 = 47`
- Expected: daily fee `47`.

#### `CalculateDailyFee_ExactlyAtCap_Returns60`

- Input data:
  - `07:00`, `08:00`, `15:30`
- Fee math:
  - three separate windows: `22 + 16 + 22 = 60`
- Expected: daily fee `60`.

#### `CalculateDailyFee_WindowWithLowerFeeFollowedByHigher_KeepsHighest`

- Input data:
  - `07:00`, `07:30`, `07:55`
- Fee math:
  - all within one window, all fee `22`, max = `22`.
- Expected: daily fee `22`.

#### `CalculateDailyFee_59MinutesApart_SameWindow`

- Input data:
  - `06:00(9)`, `06:59(16)`
- Fee math:
  - `06:59` is < `07:00` (window end) => same window.
  - highest = `16`.
- Expected: daily fee `16`.

#### `CalculateDailyFee_PassageInGapBetweenBands_TreatedAsZeroFee`

- Input data:
  - custom bands: `(360-399 => 9)`, `(420-479 => 22)`
  - passage at `06:45` (minute 405, falls in gap)
- Expected: daily fee `0`.

#### `CalculateDailyFee_DuplicateTimestamps_DoNotDoubleCharge`

- Input data:
  - `07:10`, `07:10`, `07:10`
- Fee math:
  - all same window, max `22`, charged once.
- Expected: daily fee `22`.

#### `CalculateDailyFee_PreSortedPassages_ProducesCorrectResult`

- Input data (pre-sorted):
  - `07:00`, `07:40`, `08:20`
- Fee math: same as Within60Minutes.
- Expected: daily fee `38`.

### `TollServiceTests`

#### `CalculateFee_EmptyInput_ReturnsZeroedResponse`

- Input data: `[]`
- Expected: `TotalFee=0`, `AverageFeePerDay=0`.

#### `CalculateFee_EmptyArray_ReturnsZeroedResponse`

- Input data: empty array (non-nullable contract).
- Expected: `TotalFee=0`, `AverageFeePerDay=0`.

#### `CalculateFee_WithFreeAndNonFreeDates_ChargesOnlyChargeablePassages`

- Input data:
  - configured toll-free date: `2026-01-01`
  - passages:
    - `2026-01-01 07:00` (free date)
    - `2026-01-05 07:00` (`22`)
    - `2026-01-05 08:20` (`16`)
- Fee math:
  - day `01-01` contributes `0`
  - day `01-05` contributes `22 + 16 = 38`
  - distinct days = `2`
  - average = `38 / 2 = 19`
- Expected: `TotalFee=38`, `AverageFeePerDay=19`.

#### `CalculateFee_InJuly_ReturnsZero` (Theory)

- Input data: July dates `07:00`, `08:00`.
- Flow: July exemption filters all passages.
- Expected: `TotalFee=0`, `AverageFeePerDay=0`.

#### `CalculateFee_OnWeekend_ReturnsZero` (Theory)

- Input data: Saturday `2026-01-03` and Sunday `2026-01-04`.
- Expected: `TotalFee=0`, `AverageFeePerDay=0`.

#### `CalculateFee_WithUnconfiguredYear_ThrowsYearNotConfigured`

- Input data:
  - configured year only `2026`
  - request passage `2030-01-10 07:30`
- Expected: `YearNotConfiguredException` with message containing `2030`.

#### `CalculateFee_WhenPassageCountExceedsLimit_ThrowsInvalidTollRequest`

- Input data: `1001` passages.
- Expected: `InvalidTollRequestException` with limit message.

#### `CalculateFee_ExactlyAtPassageLimit_DoesNotThrow`

- Input data: exactly `1000` passages.
- Expected: no exception, daily cap enforced.

#### `CalculateFee_WhenDateRangeExceedsLimit_ThrowsInvalidTollRequest`

- Input data: two passages spanning > 370 days.
- Expected: `InvalidTollRequestException` with range message.

#### `CalculateFee_ExactlyAtDateRangeLimit_DoesNotThrow`

- Input data: passages 370 days apart.
- Expected: no exception.

#### `CalculateFee_UtcInSummer_UsesDstOffsetForFeeBand`

- Input data: `2026-06-15T05:10:00Z`
- Flow: UTC -> CEST (UTC+2) => `07:10 local` => band `07:00-07:59` => `22`.
- Expected: `TotalFee=22`, `AverageFeePerDay=22`.

#### `CalculateFee_UtcInWinter_UsesCetOffset`

- Input data: `2026-01-12T06:10:00Z`
- Flow: UTC -> CET (UTC+1) => `07:10 local` => `22`.
- Expected: `TotalFee=22`.

#### `CalculateFee_DstSpringForward_AppliesCorrectLocalTime`

- Input data: `2026-03-30T05:10:00Z`
- Flow: DST active by March 30 => CEST (UTC+2) => `07:10 local` => `22`.
- Expected: `TotalFee=22`.

#### `CalculateFee_UtcNearYearBoundary_UsesGothenburgLocalYearForValidation`

- Input data:
  - `2025-12-31T23:30:00Z` => local `2026-01-01 00:30`
  - `2026-01-01T06:10:00Z` => local `2026-01-01 07:10`
  - configured toll-free: `2026-01-01`
- Flow: both passages become same local toll-free day.
- Expected: `TotalFee=0`, `AverageFeePerDay=0`.

#### `CalculateFee_SinglePassage_ReturnsFeeAndAverageEqual`

- Input data: `2026-01-12 07:10` (Monday).
- Expected: `TotalFee=22`, `AverageFeePerDay=22`.

#### `CalculateFee_AllPassagesOnTollFreeDays_ReturnsZeroTotal`

- Input data: holiday, Saturday, Sunday, July.
- Expected: `TotalFee=0`.

#### `CalculateFee_PassageOutsideAllBands_ReturnsZero`

- Input data: `05:00` and `19:00` on a Monday.
- Expected: `TotalFee=0`.

#### `CalculateFee_MultipleYears_ChargesEachYearWithItsOwnBands`

- Input data:
  - 2026 band: `420-479 => 22`
  - 2027 band: `420-479 => 15`
  - passages: `2026-12-29 07:10`, `2027-01-05 07:10`
- Expected: `TotalFee=37`, `AverageFeePerDay=18.5`.

#### `CalculateFee_AverageDividesAcrossAllDaysIncludingTollFree`

- Input data:
  - `2026-01-01 07:00` (holiday)
  - `2026-01-03 07:00` (Saturday)
  - `2026-01-05 07:00` (Monday, `22`)
- Fee math: total `22`, days `3`, average `22/3`.
- Expected: `TotalFee=22`, `AverageFeePerDay=22/3`.

### `YearConfigurationServiceTests`

#### `UpsertYearConfiguration_ValidData_StoresConfiguration`

- Input data:
  - year `2026`
  - fee bands: `(360-389 => 9)`, `(390-419 => 16)`
  - toll-free dates: `2026-01-01`, `2026-12-31`
- Flow: normalize + validate + persist.
- Expected: stored fee band count `2`, toll-free date count `2`.

#### `AddFeeBand_OverlappingRange_ThrowsInvalidTollRequest`

- Input data:
  - existing: `(360-389 => 9)`, `(390-419 => 16)`
  - new candidate: `(385-400 => 12)` (overlaps both)
- Expected: `InvalidTollRequestException` with overlap indicator.

#### `RemoveTollFreeDate_WhenDateExists_RemovesDate`

- Input data:
  - existing dates: `2026-01-01`, `2026-12-31`
  - remove date: `2026-12-31`
- Expected: remaining dates contain only `2026-01-01`.

#### `AddTollFreeDates_BulkAdd_AddsAllDistinctDates`

- Input data:
  - existing: `2026-01-01`
  - bulk add: `2026-12-24`, `2026-12-25`, `2026-01-01` (duplicate)
- Flow: normalize to distinct set.
- Expected: stored toll-free date count `3`.

#### `AddFeeBand_YearNotConfigured_ThrowsEntityNotFoundException`

- Input data: target year `2026` not configured, add `(360-389 => 9)`.
- Expected: `EntityNotFoundException`.

### `YearRuleConfigurationValidatorTests`

#### `Validate_InvalidYear_ThrowsInvalidTollRequestException` (Theory)

- Input data: year `<1` and `>9999`.
- Expected: `InvalidTollRequestException`.

#### `Validate_InvalidMinuteRange_ThrowsInvalidTollRequestException` (Theory)

- Input data: `fromMinute < 0`, `toMinute > 1439`, `fromMinute > toMinute`.
- Expected: `InvalidTollRequestException`.

#### `Validate_OverlappingFeeBands_ThrowsInvalidTollRequestException`

- Input data: two bands with overlapping ranges.
- Expected: `InvalidTollRequestException`.

#### `Validate_TollFreeDateOutsideYear_ThrowsInvalidTollRequestException`

- Input data: toll-free date from a different year.
- Expected: `InvalidTollRequestException`.

#### `Validate_ValidConfiguration_DoesNotThrow`

- Input data: valid config sample.
- Expected: no exception.

### `YearRulesSeedServiceTests`

#### `SeedMissingYearsFromJson_WhenYearMissing_SeedsOnceAndIsIdempotent`

- Input data:
  - seed JSON includes year `2026`
  - fee bands: `(360-389 => 9)`, `(390-419 => 16)`
  - toll-free dates: `2026-01-01`, `2026-12-31`
- Flow:
  - run seeding once, collect counts.
  - run seeding second time.
- Expected:
  - first run: fee bands `2`, dates `2`.
  - second run: counts unchanged (idempotent).

---

## Black-Box Contract Scenarios

### `GatewayContractBlackBoxTests`

#### `CalculateFee_InvalidDateQuery_ReturnsBadRequest`

- Input data: `GET /TollFee?request=not-a-date`
- Expected: HTTP `400`.

#### `CalculateFee_EmptyRequest_ReturnsZeroedPayload`

- Input data: `GET /TollFee`
- Expected: HTTP `200`, `TotalFee=0`, `AverageFeePerDay=0`.

#### `CalculateFee_UnconfiguredYear_ReturnsProblemDetailsBadRequest`

- Input data: `GET /TollFee?request=2025-01-10T07:10:00.0000000Z`
- Expected: HTTP `400`, `ProblemDetails.Status=400`, `Detail` contains `not configured`.

#### `CalculateFee_DateRangeTooLarge_ReturnsBadRequest`

- Input data: `2026-01-02T07:10:00Z`, `2027-03-01T07:40:00Z`
- Expected: HTTP `400`, `ProblemDetails.Detail` contains `range`.

#### `TestOnlyFaultEndpoint_WhenEnabled_ReturnsSanitizedProblemDetails500`

- Input data: `POST /_test/fault/throw` with valid Integration env + `X-Test-Token` header.
- Expected:
  - HTTP `500`
  - `ProblemDetails.Title="Unexpected server error"`
  - `ProblemDetails.Detail="An unexpected error occurred."`
  - no internal exception detail leaked.

#### `CalculateFee_ReadmeTodoYearValidationScenarios_ReturnExpectedContract` (Theory)

- Scenario A: `2026-02-02T07:10:00Z`, `2026-02-02T17:10:00Z` => HTTP `200`.
- Scenario B: `2025-01-10T07:10:00Z` => HTTP `400`.
- Scenario C: `2026-02-02T07:10:00Z`, `2025-12-30T07:10:00Z` => HTTP `400`.
- Scenario D: `2027-01-07T07:10:00Z` => HTTP `400`.

#### `CalculateFee_ConfiguredYearResponse_IsStableAcrossRepeatedCalls`

- Input data: `2026-02-02T07:10:00Z` (`22`), `2026-02-02T17:10:00Z` (`16`)
- Flow: call endpoint twice, compare payloads.
- Expected: total `38`, average `38`, both responses equal.

#### `CalculateFee_LargeInput_CompletesWithinReasonableTime`

- Input data: 180 generated timestamps from base `2026-08-03T06:00:00Z`.
- Expected: HTTP `200`, response time < `4000ms`.

#### `ConfigApi_GetYearConfiguration_ReturnsSeeded2026Dates`

- Input data: `GET /configuration/years/2026`
- Expected: HTTP `200`, `Year=2026`, toll-free date count `16`, set equality with documented 2026 exempt day list.

#### `ConfigApi_GetYearConfiguration_UnconfiguredYear_ReturnsNotFound`

- Input data: `GET /configuration/years/2098`
- Expected: HTTP `404`.

#### `ConfigApi_UpsertYearConfiguration_MalformedJson_ReturnsBadRequest`

- Input data: truncated JSON body to `PUT /configuration/years/2051`.
- Expected: HTTP `400`.

#### `ConfigApi_AddFeeBand_InvalidAmountType_ReturnsBadRequestProblemDetails`

- Input data: `"amount": "invalid"` (string instead of int).
- Expected: HTTP `400`.

#### `ConfigApi_RemoveAndReAddTollFreeDate_InvalidatesCacheAndAffectsFee`

- Input data:
  - calculate `2026-01-01T07:10:00Z`
  - `DELETE /configuration/years/2026/toll-free-dates/2026-01-01`
  - `POST /configuration/years/2026/toll-free-dates` body `{ "date": "2026-01-01" }`
- Expected flow:
  - before remove => total `0`
  - after remove => total > `0`
  - after re-add => total `0`.

#### `ConfigApi_AddOverlappingFeeBand_ReturnsBadRequest`

- Input data: `POST /configuration/years/2026/fee-bands` body `{ "fromTime": "0620", "toTime": "0640", "amount": 12 }`
- Expected: HTTP `400`, `ProblemDetails.Detail` contains `overlap`.

#### `ConfigApi_RemoveFeeBand_UnconfiguredYear_ReturnsNotFoundProblemDetails`

- Input data: `DELETE /configuration/years/2099/fee-bands/0600/0629`
- Expected: HTTP `404`, `Title="Resource not found"`, detail mentions target year.

#### `ConfigApi_UpdateTollFreeDate_MissingDate_ReturnsNotFoundProblemDetails`

- Input data: `PUT /configuration/years/2026/toll-free-dates/2026-02-10` body `{ "date": "2026-02-11" }`
- Expected: HTTP `404`, `Title="Resource not found"`, detail contains `not found`.

#### `ConfigFlow_UnconfiguredYearThenConfigureThenRetry_ReturnsExpectedFee`

- Input data:
  - year `2044`, calc request `2044-01-11T07:10:00Z`
  - configure: default 9 fee bands + toll-free `2044-01-01`
- Expected:
  - before configuration => HTTP `400`
  - after configuration => HTTP `200`, `07:10 => 22`, total `22`.

#### `ConfigFlow_MixedYearRequestThenProgressiveConfigure_BecomesSuccessful`

- Input data:
  - years `2046`, `2047`
  - mixed request: `2046-01-10T07:10:00Z`, `2047-01-10T07:10:00Z`
- Expected:
  - after configuring only first year => HTTP `400`
  - after configuring second year => HTTP `200`.

#### `ConfigApi_SingleAndBulkTollFreeDateUpdates_AffectCalculation`

- Input data:
  - year `2048`
  - single: calculate `2048-02-10T07:10:00Z`, add `{ "date": "2048-02-10" }`
  - bulk: calculate `2048-02-11T07:10:00Z`, add `{ "dates": ["2048-02-11"] }`
- Expected:
  - before single add => `22`, after => `0`
  - before bulk add => `22`, after => `0`.

#### `ConfigApi_SingleAndBulkFeeBandUpdates_AffectCalculation`

- Input data:
  - year `2049`
  - update: `PUT .../fee-bands/0700/0759` body `{ "amount": 25 }`
  - bulk add: `POST .../fee-bands/bulk` body `{ "feeBands": [{ "fromTime": "1830", "toTime": "1840", "amount": 5 }] }`
- Expected:
  - `07:10` before update => `22`, after => `25`
  - `18:35` before bulk => `0`, after => `5`.

#### `ConfigApi_YearUpsert_IsIdempotentForCalculation`

- Input data: year `2050`, same PUT body twice, calc `2050-01-12T07:10:00Z`.
- Expected: both PUTs => `204`, calc => total `22`.

---

## Black-Box Real-Life Scenarios

### `GatewayRealLifeBlackBoxTests`

#### `Gateway_SmokeCheck_ReturnsSuccessOrClientError`

- Input data: `GET /TollFee`
- Expected: status code < `500`.

#### `Gateway_StatementLikeDayScenario_ReturnsExpectedTotal`

- Input data:
  - `2026-02-02T07:10:00Z`, `2026-02-02T07:40:00Z`
  - `2026-02-02T17:10:00Z`, `2026-02-02T17:40:00Z`
- Fee math:
  - morning window: `07:10(22)` + `07:40(22)` => one charge = `22`
  - evening window: `17:10(16)` + `17:40(16)` => one charge = `16`
  - day total = `22 + 16 = 38`
- Expected: total `38`, average `38`.

#### `Gateway_WeekScenario_ReturnsExpectedAggregate`

- Input data:
  - `2026-02-02T07:10:00Z`, `2026-02-02T17:10:00Z`
  - `2026-02-03T07:10:00Z`, `2026-02-03T17:10:00Z`
  - `2026-02-04T07:10:00Z`, `2026-02-04T17:10:00Z`
- Fee math: each day `22 + 16 = 38`, 3 days => `114`.
- Expected: total `114`, average `38`.

#### `Gateway_MonthScenario_ReturnsExpectedAggregate`

- Input data: `February2026Passages` (74 timestamps across 20 working days).
- Fee math:
  - 13 days with pattern `07:10+07:40+17:10+17:40` or `07:10+17:10` => `38` each
  - 4 days with pattern `06:40+06:50` => `16` each
  - 3 days with pattern `06:40+15:10` => `32` each
  - `13*38 + 4*16 + 3*32 = 494 + 64 + 96 = 654`
- Expected: total `654`.

#### `Gateway_CalculatedHolidayBootstrap_HolidayIsTollFree`

- Input data: `2026-01-01T07:10:00Z`
- Expected: total `0`.

#### `Gateway_DetailedRealUsageScenarios_ReturnExpectedTotalsAndAverages` (Theory)

- `weekday_commute_basic`
  - inputs: `2026-01-12T07:10:00Z`, `2026-01-12T17:10:00Z`
  - expected: total `38`, average `38`
- `peak_cluster_inside_60min`
  - inputs: `06:20(9)`, `06:50(16)`, `07:10(22)` on `2026-01-12`
  - fee math: one window max = `22`
  - expected: total `22`, average `22`
- `exact_60min_boundary_two_charges`
  - inputs: `06:10(9)`, `07:10(22)` on `2026-01-12`
  - fee math: exactly 60 min => two windows => `9 + 22 = 31`
  - expected: total `31`, average `31`
- `daily_cap_is_enforced`
  - inputs: `07:10`, `08:30`, `09:45`, `15:10`, `16:30`, `17:10`, `18:10` on same day
  - fee math: raw `22+9+9+16+22+9 = 87` => cap `60`
  - expected: total `60`, average `60`
- `weekend_is_toll_free`
  - inputs: `2026-01-10` (Saturday)
  - expected: total `0`, average `0`
- `july_is_toll_free`
  - inputs: `2026-07-02`
  - expected: total `0`, average `0`
- `holiday_day_is_free_jan1`
  - inputs: `2026-01-01T07:10:00Z`, `2026-01-02T07:10:00Z`
  - fee math: Jan 1 free, Jan 2 = `22`, days = 2
  - expected: total `22`, average `11`
- `day_before_holiday_is_free_jan5`
  - inputs: `2026-01-05T07:10:00Z`, `2026-01-07T07:10:00Z`
  - fee math: Jan 5 (day-before-Epiphany) free, Jan 7 = `22`, days = 2
  - expected: total `22`, average `11`
- `cross_midnight_split_across_days`
  - inputs: `2026-01-12T23:50:00Z`, `2026-01-13T00:10:00Z`, `2026-01-13T07:30:00Z`
  - fee math: Jan 12 `23:50` => no band => `0`. Jan 13 `00:10` => no band => `0`, `07:30` => `22`. Total `22`, days 2.
  - expected: total `22`, average `11`
- `unordered_and_duplicate_timestamps`
  - inputs: `09:40`, `07:30`, `07:30`, `08:20` (unordered + duplicate)
  - fee math: sorted => `07:30(22), 07:30(22), 08:20(16), 09:40(9)`. Window 1 max `22`, window 2 `9`. Total `31`.
  - expected: total `31`, average `31`
- `multi_day_mixed_charge_and_free_days`
  - inputs: `2026-06-30T17:10:00Z`, `2026-07-01T07:10:00Z`, `2026-07-02T17:10:00Z`
  - fee math: Jun 30 (Tue) `17:10 => 16`. Jul 1, Jul 2 => July free. Total `16`, days 3.
  - expected: total `16`, average `5.3333335`
- `two_day_statement_pattern`
  - inputs: Feb 2 (`07:10, 07:40, 17:10, 17:40`) + Feb 9 (`06:40, 06:50`)
  - fee math: Feb 2 = `22 + 16 = 38`. Feb 9 = `16`. Total `54`, days 2.
  - expected: total `54`, average `27`

#### `Gateway_MigratedComplexScenarios_ReturnExpectedTotalsAndAverages` (Theory)

Case 1:
- inputs: Jan 12 (`07:30, 08:20, 09:40`), Jan 13 (`06:10, 06:50, 15:20`), Jan 14 (`17:10, 17:50`), Jan 17 (`07:30`), Jan 18 (`07:30`)
- fee math:
  - Jan 12: `22 + 9 = 31`
  - Jan 13: `16 + 16 = 32`
  - Jan 14: `16`
  - Jan 17 (Sat): `0`
  - Jan 18 (Sun): `0`
- expected: total `79`, average `15.8`

Case 2:
- inputs: Jun 29 (`07:30, 08:40`), Jun 30 (`15:40, 16:20`), Jul 1 (`07:30`), Jul 15 (`15:40`), Aug 3 (`06:20, 06:45, 18:10`)
- fee math:
  - Jun 29: `22 + 9 = 31`
  - Jun 30: `22`
  - Jul 1, Jul 15: July free => `0`
  - Aug 3: `16 + 9 = 25`
- expected: total `78`, average `15.6`

Case 3:
- inputs: Jan 5-9 (holidays + weekdays + daily cap)
- fee math:
  - Jan 5 (toll-free): `0`
  - Jan 6 (toll-free): `0`
  - Jan 7: `22`
  - Jan 8: `22 + 22 = 44`
  - Jan 9: `22 + 16 + 22 + 16 = 76` => cap `60`
- expected: total `126`, average `25.2`

Case 4:
- inputs: `09:40, 07:30, 07:30, 08:20` (unordered single day)
- expected: total `31`, average `31`

Case 5:
- inputs: `23:50, 00:10, 07:30` (cross-midnight)
- expected: total `22`, average `11`

#### `Gateway_January2026RandomizedFullCalculationScenarios_MatchExpected` (Theory)

Scenario 1: `january_randomized_holiday_weekend_boundary_mix`
- Input data:
  - `2026-01-01T07:10:00Z`
  - `2026-01-02T06:20:00Z`, `2026-01-02T06:50:00Z`, `2026-01-02T07:10:00Z`, `2026-01-02T15:10:00Z`
  - `2026-01-03T07:10:00Z`
  - `2026-01-05T07:10:00Z`
  - `2026-01-06T17:10:00Z`
  - `2026-01-07T06:10:00Z`, `2026-01-07T07:10:00Z`, `2026-01-07T18:20:00Z`
  - `2026-01-12T07:10:00Z`, `2026-01-12T07:40:00Z`, `2026-01-12T08:20:00Z`, `2026-01-12T17:40:00Z`
  - `2026-01-18T07:30:00Z`
  - `2026-01-21T15:10:00Z`, `2026-01-21T15:20:00Z`, `2026-01-21T16:30:00Z`
  - `2026-01-29T18:31:00Z`
- Fee math:
  - `01-01` holiday => `0`
  - `01-02`: `06:20(9), 06:50(16), 07:10(22)` one window => `22`, `15:10(16)` new window => `+16`, day total `38`
  - `01-03` Saturday => `0`
  - `01-05` day-before-holiday => `0`
  - `01-06` holiday => `0`
  - `01-07`: `06:10(9)` window ends `07:10`. `07:10(22)` exactly 60 min => new window. `18:20(9)` new window. Day total `9 + 22 + 9 = 40`
  - `01-12`: `07:10(22), 07:40(22)` same window => `22`. `08:20(16)` new window => `+16`. `17:40(16)` new window => `+16`. Day total `54`
  - `01-18` Sunday => `0`
  - `01-21`: `15:10(16), 15:20(16)` same window => `16`. `16:30(22)` new window => `+22`. Day total `38`
  - `01-29`: `18:31` outside all bands => `0`
- Expected: total `170`, distinct days `10`, average `17`.

Scenario 2: `january_randomized_daily_cap_and_boundary_edges`
- Input data:
  - `2026-01-08T06:00:00Z`, `06:29`, `06:30`, `07:15`, `08:00`, `08:31`
  - `2026-01-08T15:05:00Z`, `15:35`, `16:45`, `17:10`, `18:00`
  - `2026-01-24T08:10:00Z`, `16:10`
  - `2026-01-26T07:10:00Z`
- Fee math:
  - `01-08`: `06:00(9)` window end `07:00`. `06:29(9)` same. `06:30(16)` same => max `16`. `07:15(22)` new window end `08:15`. `08:00(16)` same => max `22`. `08:31(9)` new. `15:05(16)` new end `16:05`. `15:35(22)` same => max `22`. `16:45(22)` new end `17:45`. `17:10(16)` same => max `22`. `18:00(9)` new. Raw total `16 + 22 + 9 + 22 + 22 + 9 = 100` => cap `60`
  - `01-24` Saturday => `0`
  - `01-26`: `07:10 => 22`
- Expected: total `82`, distinct days `3`, average `27.333334`.
