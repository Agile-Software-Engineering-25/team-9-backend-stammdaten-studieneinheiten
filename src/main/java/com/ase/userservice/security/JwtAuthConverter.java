// based on this tutorial: https://www.javacodegeeks.com/2025/07/spring-boot-keycloak-role-based-authorization.html


package com.ase.userservice.security;

import org.springframework.core.convert.converter.Converter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.lang.NonNull;
import java.util.Collection;
import java.util.stream.Collectors;

public class JwtAuthConverter implements Converter<Jwt, Collection<GrantedAuthority>> {

    @Override
    public Collection<GrantedAuthority> convert(@NonNull Jwt jwt) {
        var roles = jwt.getClaimAsStringList("groups");

        // you can check the roles here if you want to
        //for (String role : roles) {
        //System.out.println("Role from JWT: " + role);
        // }
        return roles.stream()
                .map(role -> new SimpleGrantedAuthority("ROLE_" + role.toUpperCase()))
                .collect(Collectors.toList());
    }
}