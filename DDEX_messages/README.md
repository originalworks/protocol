# DDEX messages

The Original Works protocol uses the industry standard DDEX to communicate.

* ERN:
    * NewReleaseMessage --> To register an ISRC with our without an ISWC
    * UpdateReleaseMessage --> To update information about an existing release
    * TakedownMessage --> To remove a release
* MWN MusicalWorkNotificationMessage:
    * To register a ISWC
    * To link a ISWC to an ISRC
* DSR:
    * To report past revenues of an asset.
* CDN:
    * Future implementation of right claims ([Issue #29](https://github.com/originalworks/protocol/issues/29))

## ERN

We use ERN v.4.3

https://ern.ddex.net/electronic-release-notification-message-suite-part-1-definitions-of-messages/ 

An example ERN message is available [here](./ERN_NewReleaseMessage_example.xml).

Types of ERN Messages:

`NewReleaseMessage`: Used to notify about a new release.

`UpdateReleaseMessage`: Used to update information about an existing release. This can include changes to the release metadata, artist information, or other related data.

`TakedownMessage`: Used to notify a recipient that a previously released product should no longer be available. This is typically used for removing releases from digital service providers.

`PurgeReleaseMessage`: Used to purge a release from the recipient’s system. Unlike the TakedownMessage, which simply marks the release as inactive, the PurgeReleaseMessage is used to completely remove the release information.

`RightShareNotificationMessage`: Used to communicate information about the rights holders and the shares they hold for a particular release or set of releases. This is essential for ensuring that royalties are correctly allocated and distributed.

`ReleaseStatusChangeMessage`: Used to notify about changes in the status of a release. This could include changes such as a release becoming active or inactive.


## MWN

MWN messages are using to communicate an ISWC and link it to previously sent ISRCs.

Key and unique values in the registry will be the following fields:
* `MusicalWork`->`MusicalWorkID`-> **`ISWC`**
* `MusicalWork`-> `RightShare` -> **`RightType`**
* `MusicalWork`-> `RightShare` -> **`Territory`**

We also have `SharePercentage` we need to handle. TODO.


Summary of elements:
`MessageHeader`: Contains metadata about the message, such as IDs, creation date, sender, and recipient.
`MusicalWork`: Contains details about the musical work, including its ID (ISWC), title, composer, and rights information.
`RightShare` Encapsulates information about the specific rights associated with the musical work, including the proprietary ID, controller, and types of rights.
`LinkedResource`: Links the musical work to the associated sound recording using the ISRC.


## DSR

The DSR messages are designed to facilitate the exchange of sales and usage data between digital service providers (DSPs) and rights holders.

## Fields

All fields are tagged as `<!-- Compulsory -->` or `<!-- Optional -->`.

`<!-- Compulsory -->` are compulsary fields, and messages will be rejected if they are not included.
`<!-- Optional -->` can either exist or not.
`<!-- Needs to exist --> ` is a field that needs to exist in either the private or the public part of the message, but not required on both.
