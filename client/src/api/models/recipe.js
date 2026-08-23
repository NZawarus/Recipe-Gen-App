// Recipe model interface
export class Recipe {
  constructor(user_id, recipe_name, recipe_content) {
    this.user_id = user_id;
    this.recipe_name = recipe_name;
    this.recipe_content = recipe_content;
  }
}

export class RecipeCreate {
  constructor(recipe_name, recipe_content) {
    this.recipe_name = recipe_name;
    this.recipe_content = recipe_content;
  }
}

export class RecipeGet {
  constructor(recipe_id = null, recipe_name = null, recipe_content = null) {
    this.recipe_id = recipe_id;
    this.recipe_name = recipe_name;
    this.recipe_content = recipe_content;
  }
}

export class RecipeUpdate {
  constructor(recipe_name = null, recipe_content = null) {
    this.recipe_name = recipe_name;
    this.recipe_content = recipe_content;
  }
}

export class RecipeDelete {
  constructor(recipe_id) {
    this.recipe_id = recipe_id;
  }
} 