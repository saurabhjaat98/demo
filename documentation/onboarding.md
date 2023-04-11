# Self Onboarding Flow

1. `Click on Signup`
2. `User will enter` : First name, Last Name, Email and Organisation name
3. `Click on Submit button`
4. `Self Onboarding Api will be triggered which includes:`
    1. Request will be validated by SelfOnnboarding Pydantic model
    2. User will be created in Keycloak only
    3. Organisation will be created in Keycloak (as Group), and then in Mongo
    4. User will be added in the group in Keycloak
    5. User will be assigned org-admin role in Keycloak
    6. A verification email is sent to the user so that user can set a login password.
    7. We will set `profile_complete` attribute to as `False`.

# After Verification Flow:

1. `User will enter username and password and clicks on Login`.
2. `If the user is org-admin and his profile_completed attribute is` **False**:
3. `User will enter`:
    1. **Description** : Optional
    2. **Default_cloud**: Optional
    3. **Communication Address**
    4. **Billing Address**
    5. **TAN Number**
    6. **GST Number**
4. `Complete Profile Api will be called`.
5. `User's profile_completed attribute will be checked if its` **True** `or` **False**
6. `If` **true** `we will return 422 error otherwise will continue the flow`
7. `We will get the user orgs with the logged in user token`.
8. `We will set the default cloud if it is provided otherwise it will be same as before and will be set to the header`
9. `A subgroup(Project) will be created in Keycloak and
     Project will be created in Mongo with` **default** `name`
10. `User will be created in Cloud and then in ceph`
11. `User will be added to the project`
12. `We will set` **profile_completed** `as` **True**.
13. `User Profile will be returned which included user, org and his project information.`
