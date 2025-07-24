# 16: Deployment to Production Orchestrators

This section addresses the process of taking the application's build artifacts – most commonly **container images** built in Topic 11, or less commonly, Python packages built in Topic 09 for certain environments – and deploying them to scalable production environments managed by dedicated orchestration platforms.

## Goals Addressed

- Ensure that the template's build artifacts (container images, Python packages) are **compatible with and consumable by** standard production deployment tools and platforms.
- Acknowledge that defining **full production infrastructure deployment configurations** is complex, highly environment-specific, and outside the direct scope of this general Python project template.
- Provide guidance on how to approach deployment and mention common types of tools/platforms used for production orchestration.

## Evaluation Criteria (for Artifact Readiness and Guidance)

Since this template does _not_ provide production-ready infrastructure configuration out-of-the-box, we evaluate based on the compatibility of its _outputs_ and the quality of its _guidance_.

- **Artifact Compatibility:** Are the outputs from the template's build workflows (container images, Python packages) standard formats that can be used as inputs by common production deployment tools?
- **Scope Acknowledgment:** Does the template's documentation clearly define the boundary of its scope, acknowledging that full production deployment setup is external and complex?
- **Guidance Quality:** Does the template's documentation provide clear, helpful guidance on how users can transition from the template's outputs to a production deployment using common tools and patterns?
- **Relevance of Mentioned Tools:** Are the types of tools/platforms mentioned in the guidance appropriate and widely used for production orchestration?

## Tools and Platforms Evaluated

We don't evaluate specific tools _for inclusion as configuration files in the template_ in this section. Instead, we discuss the _types of tools and platforms that consume the template's outputs_ and evaluate how well the template ensures its outputs are compatible with them, and the quality of the guidance it provides regarding these tools.

### Type of Tool/Platform 1: Container Orchestration Platforms (e.g., Kubernetes, Amazon ECS, Google GKE, Azure AKS)

- **Description:** Scalable platforms designed to automate the deployment, scaling, and management of containerized applications in production. Kubernetes is the dominant player. Cloud providers offer managed services based on or similar to Kubernetes.
- **Role:** They consume container images (built in Topic 11, pushed to registries in Topic 14) and run them as instances (pods, tasks), managing networking, storage, and scaling.
- **Compatibility with Template Outputs:** Excellent. The template's focus on building **standard container images (Topic 11, using `Dockerfile`)** ensures they are universally compatible inputs for these platforms.
- **Complexity vs. Template Scope:** Very High. Configuring these platforms involves extensive YAML manifests (Deployments, Services, Ingress, etc.), infrastructure setup (clusters, nodes, networking), and operational concerns (monitoring, logging, scaling). This is **highly specific to the target infrastructure and deployment strategy** and is far beyond the scope of a general Python project template.

### Type of Tool/Platform 2: Configuration Management for Orchestration (e.g., `Helm`{helm<>} for Kubernetes, Kustomize, CloudFormation, Terraform)

- **Description:** Tools that manage the complex configurations required by orchestration platforms. `Helm`{helm<>} is popular for packaging Kubernetes applications (sets of manifests).
- **Role:** They manage and deploy the configuration manifests _that tell the orchestrator what containers to run_. They consume container images (via image names/tags in the manifests).
- **Compatibility with Template Outputs:** Excellent. These tools are designed to use standard container image references, directly compatible with images built by the template. They can also reference package versions indirectly (e.g., in a Helm chart that deploys a container built from a specific package version).
- **Complexity vs. Template Scope:** Very High. Creating and maintaining Helm charts or other infrastructure-as-code is complex, requires understanding the orchestration platform and deployment strategy, and is external to the core application development process. Providing comprehensive templates for this is infeasible in a general Python project template.

### Type of Tool/Platform 3: Continuous Delivery Tools/Platforms (e.g., `Argo CD`{argocd<>} for Kubernetes, Spinnaker, Jenkins CD)

- **Description:** Tools and platforms that automate the flow of code from commit to production deployment, often implementing GitOps principles (`Argo CD`{argocd<>}). They monitor source repositories and orchestrate deployment on target platforms based on changes.
- **Role:** They pull built artifacts (container images, potentially manifests) and deploy them to target environments, integrating with container registries (output of Topic 14) and orchestration platforms (Type 1). They _do not build the initial artifacts_.
- **Compatibility with Template Outputs:** Excellent. These tools are designed to consume built container images (via registries) and deployment manifests (generated by Type 2 tools or managed in separate repos), directly compatible with the template's CD output.
- **Complexity vs. Template Scope:** Very High. Configuring these platforms requires understanding the entire deployment pipeline and target infrastructure. Setting up Argo CD itself involves running Kubernetes manifests, etc. This is external to the core application template.

### Type of Tool/Platform 4: Serverless Deployment (e.g., AWS Lambda, Google Cloud Run, Azure Functions, Vercel)

- **Description:** Platforms that run application code (often Python functions or web services) without requiring explicit server management. Code can be deployed as packages, ZIP files, or container images.
- **Role:** They run the application code directly, scaling automatically.
- **Compatibility with Template Outputs:** Excellent. These platforms are compatible with Python packages (sdist, wheel - Topic 09 output) or container images (Topic 11 output), which they can deploy directly.
- **Complexity vs. Template Scope:** Moderate to High. Deployment methods vary significantly by platform. Configuration is specific to the chosen serverless provider. While simpler than full Kubernetes, still external and environment-specific.

## Chosen Approach

- **Focus on Artifact Readiness:** Ensure the template's workflows reliably build and publish **standard, consumable artifacts** (container images from Topic 11, Python packages from Topic 09) suitable as inputs for common production deployment tools.
- **Provide Documentation and Guidance:** Include clear documentation that acknowledges the external and complex nature of production deployment and guides users on how the template's outputs can be used with **common types of deployment tools and platforms**, mentioning examples like `Docker Compose`{docker<>} (Topic 15 for local context), Kubernetes orchestration (raw manifests, `Helm`{helm<>}), GitOps tools (`Argo CD`{argocd<>}), and serverless options. Do **NOT** include production deployment manifests or specific cloud configuration files within the template's core structure by default.

## Justification for the Choice

This approach provides maximum value to the user within the scope of a general Python project template while being realistic about the complexity of production deployment:

1.  **Ensuring Compatibility:** By prioritizing the generation of **standard, high-quality build artifacts** (container images, packages) in Topics 09 and 11, the template fulfills the fundamental requirement that its outputs **CAN be consumed** by any standard production deployment method (addressing **Artifact Compatibility**). This is the template's core responsibility related to deployment readiness.
2.  **Clear Scope Definition:** Explicitly stating that full production deployment configuration is complex and external to the template prevents users from expecting infrastructure-specific solutions within the base template. This sets realistic expectations (addressing **Scope Acknowledgment**). This aligns with **"Special cases should be allowed, but at their own expense"**, treating full infra config as a complex external special case.
3.  **Empowering Users with Guidance:** Providing documentation that lists common types of deployment tools and platforms (Kubernetes, ECS, GKE, AKS, Lambda, Cloud Run, App Services, `Helm`{helm<>}, `Argo CD`{argocd<>}, `docker-compose`{docker<>} for local/simple reference) and explains how the template's standard outputs fit into these ecosystems gives users the knowledge to **choose and implement their specific deployment solution** (addressing **Guidance Quality** and **Relevance of Mentioned Tools**). It leverages the work done in Areas 09, 11, and 14.

By focusing on producing consumable artifacts and providing helpful guidance on how to integrate them into the wider deployment landscape, the template ensures its outputs are production-ready inputs for whatever external infrastructure and orchestration layer the user chooses, without adding overly complex or highly context-specific configurations to the template's core.

## Interactions with Other Topics

- **Packaging Build (09):** Produces Python packages (sdist/wheel) which can be deployment artifacts for serverless or other methods.
- **Application Container Building (11):** Produces container images, the most common deployment artifact for orchestrated environments.
- **Task Automation (12), CI Orchestration (13), CD Orchestration (14):** These workflows automate the creation and _potential_ publication of the artifacts needed for production deployment.
- **Container Orchestration (Local) (15):** While focused on local use, `docker-compose`{docker<>} concepts and tools serve as a stepping stone or simplified analogy for understanding multi-service orchestration concepts used in production platforms. It's a related tool category mentioned in guidance.
