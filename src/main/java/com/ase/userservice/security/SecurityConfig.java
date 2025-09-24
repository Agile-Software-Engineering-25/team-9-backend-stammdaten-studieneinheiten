// based on this tutorial: https://www.javacodegeeks.com/2025/07/spring-boot-keycloak-role-based-authorization.html

package com.ase.userservice.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;
 
@Configuration
@EnableMethodSecurity
public class SecurityConfig {
 
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        JwtAuthenticationConverter jwtConverter = new JwtAuthenticationConverter();
        jwtConverter.setJwtGrantedAuthoritiesConverter(new JwtAuthConverter());
        
 
        //the role always has to be capitalized
        http
          .csrf(csrf -> csrf.disable()) // Disable CSRF for API endpoints isnt needed for our purpose since we are not using cookies for auth
          .authorizeHttpRequests(authorize -> authorize
            .requestMatchers("/demo").hasRole("DEFAULT-ROLES-SAU")
            .requestMatchers("/admin/**").hasRole("admin")
            .anyRequest().authenticated())
          .oauth2ResourceServer(oauth2 -> oauth2
            .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtConverter)));
        return http.build();
    }
}