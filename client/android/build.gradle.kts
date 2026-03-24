buildscript {
    repositories {
        google()
        mavenCentral()
        maven("https://chaquo.com/maven")
    }
    dependencies {
        classpath("com.chaquo.python:gradle:17.0.0")
    }
}

plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
