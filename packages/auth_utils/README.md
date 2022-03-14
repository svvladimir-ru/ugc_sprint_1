## Utils for authorization validation

class **AuthRequired**(permissions, condition, token_optional, permissions_optional)  

    A tool (a dependency class) to validate user authentication and permission for endpoint via Auth service.

    Depending on parameters, it validates token, permissions (if any) and based on that can prevent access
    to an endpoint with corresponding http status codes and messages if needed, or it can provide access and
    just provide auth info on whether token/permissions are valid or not if corresponding options are enabled.

    If permissions are not satisfied, access to endpoint is denied with 403 code in strict mode. Or provided
    with permissions_valid set to false.
    One can specify any number of permissions or a condition for more sophisticated requirements.
    When several permissions are specified, all of them are supposed to be required.
    Whatever condition or permissions are specified, superuser permission 'any_any' is always implicitly
    added as alternative requirement, which means any permissions requirement is satisfied for superuser.
    
    Auth service host and port are configured via env variables AUTH_HOST and AUTH_PORT. In case of local token 
    validation, signature key is configured via AUTH_SECRET_KEY env variable.