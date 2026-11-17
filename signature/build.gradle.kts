plugins {
    id("com.android.library")
    id("maven-publish")
}

android {
    namespace = "com.nijatva.signature"
    compileSdk = 34

    defaultConfig {
        // The kit uses framework APIs only; LOLLIPOP is enough.
        minSdk = 21
        consumerProguardFiles("consumer-rules.pro")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    publishing {
        singleVariant("release") {
            withSourcesJar()
        }
    }
}

dependencies {
    // Deliberately none: the signature kit is plain framework Java, so any app in the
    // suite can consume it without pulling in AndroidX, Compose or Kotlin.
}

group = "com.nijatva"
version = "1.0.0"

publishing {
    publications {
        register<MavenPublication>("release") {
            afterEvaluate { from(components["release"]) }
            artifactId = "signature"
        }
    }
    repositories {
        // `./gradlew :signature:publishToMavenLocal` for local app builds.
        // Add a GitHub Packages repository here when the suite gets CI.
        mavenLocal()
    }
}
