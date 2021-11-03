import { expect } from "chai";
import { shallowMount } from "@vue/test-utils";
import HomeView from "@/views/HomeView.vue";

describe("HelloWorld.vue", () => {
  it("renders props.msg when passed", () => {
    const wrapper = shallowMount(HomeView);
    expect(wrapper.text()).to.include("features");
  });
});
