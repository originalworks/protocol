# DDEX messages

The Original Works protocol uses the industry standard DDEX to communicate.

## ERN

We use ERN v.4.3

https://ern.ddex.net/electronic-release-notification-message-suite-part-1-definitions-of-messages/ 

A simple ERN message will contain these fields:

```xml
<MessageHeader></MessageHeader>
<ResourceList></ResourceList>
<DealList></DealList>
```

Type of ERN Messages:

`NewReleaseMessage`: Used to notify about a new release.

`UpdateReleaseMessage`: Used to update information about an existing release. This can include changes to the release metadata, artist information, or other related data.

`TakedownMessage`: Used to notify a recipient that a previously released product should no longer be available. This is typically used for removing releases from digital service providers.

`PurgeReleaseMessage`: Used to purge a release from the recipient’s system. Unlike the TakedownMessage, which simply marks the release as inactive, the PurgeReleaseMessage is used to completely remove the release information.

`RightShareNotificationMessage`: Used to communicate information about the rights holders and the shares they hold for a particular release or set of releases. This is essential for ensuring that royalties are correctly allocated and distributed.

`ReleaseStatusChangeMessage`: Used to notify about changes in the status of a release. This could include changes such as a release becoming active or inactive.

