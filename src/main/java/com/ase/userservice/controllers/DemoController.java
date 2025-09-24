package com.ase.userservice.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DemoController {
	// to manage access, add route rules in security/SecurityConfig.java like in the
	// examples
	@GetMapping("/demo")
	public String demo() {
		return "Hello from DemoController!";
	}
}