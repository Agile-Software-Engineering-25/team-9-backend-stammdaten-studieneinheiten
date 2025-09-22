package com.ase.userservice.entities;

import java.util.ArrayList;

public class User {
    public int exp;
    public int iat;
    public int auth_time;
    public String jti;
    public String iss;
    public String aud;
    public String sub;
    public String typ;
    public String azp;
    public String sid;
    public String at_hash;
    public String acr;
    public String upn;
    public boolean email_verified;
    public String name;
    public ArrayList<String> groups;
    public String preferred_username;
    public String given_name;
    public String family_name;
    public String email;
}
